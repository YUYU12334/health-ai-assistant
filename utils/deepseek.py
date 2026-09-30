"""DeepSeek 大模型接入与演示模式回退。

- 通过 OpenAI 兼容接口调用 DeepSeek（https://api.deepseek.com）。
- API Key 从 st.secrets 或环境变量读取。
- 未配置 Key 或缺少 openai 依赖时，自动回退到内置演示模式，
  保证作品“开箱即可运行、可在线演示”。
"""

from __future__ import annotations

import os
import time
from typing import Generator

import streamlit as st

MODEL = "deepseek-chat"
BASE_URL = "https://api.deepseek.com"

SYSTEM_PROMPT = """你是「康伴」——一名温和、专业、负责任的 AI 健康问答助手。你的定位是健康科普与健康管理建议，而不是医生。

请严格遵守以下规则：
1. 你不提供疾病诊断、不开具处方、不替代医生的面诊。回答时用通俗易懂的语言，必要时分点说明。
2. 涉及紧急、危重症状（如剧烈胸痛、呼吸困难、大出血、意识丧失、中风征兆、自杀自残倾向等），
   必须第一时间强烈建议拨打 120 或就近急诊，并给出简短的就医前注意事项。
3. 回答内容应基于公认的医学常识，避免绝对化、避免夸大疗效；不确定时明确说“建议咨询专业医生”。
4. 语气温暖、克制，不制造焦虑。回答结尾如涉及就医判断，可附一句“以上仅供参考，不能替代专业诊疗”。
5. 用户可能使用中文提问，请始终用中文回答。"""


def get_api_key() -> str | None:
    """优先从 Streamlit secrets 读取，其次环境变量。"""
    key = None
    try:
        key = st.secrets.get("DEEPSEEK_API_KEY")
    except Exception:
        key = None
    if not key:
        key = os.environ.get("DEEPSEEK_API_KEY")
    if key and key.startswith("sk-") and "xxxx" not in key:
        return key.strip()
    return None


def is_configured() -> bool:
    return get_api_key() is not None


def _build_client():
    """惰性导入 openai 并构建客户端，未安装时抛 ImportError 由调用方回退。"""
    from openai import OpenAI

    return OpenAI(api_key=get_api_key(), base_url=BASE_URL)


def _model_messages(messages: list[dict]) -> list[dict]:
    """构造发送给大模型的对话上下文。

    安全护栏提示（紧急/危机）是给用户看的界面提示，不作为模型上下文传入，
    否则会污染后续对话的语义。
    """
    return [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m.get("kind") not in ("emergency", "crisis") and m.get("content")
    ]


def stream_chat(messages: list[dict]) -> Generator[str, None, None]:
    """流式返回助手回复。不可用或出错时回退到演示模式。"""
    if not is_configured():
        yield from _demo_stream(messages)
        return

    try:
        client = _build_client()
    except ImportError:
        yield from _demo_stream(messages)
        return

    payload = [{"role": "system", "content": SYSTEM_PROMPT}, *_model_messages(messages)]
    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=payload,
            stream=True,
            temperature=0.6,
            max_tokens=1200,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as exc:  # noqa: BLE001 - 任何调用异常都回退，保证演示不中断
        yield f"\n\n> :orange[（大模型调用失败，已切换为演示模式：{type(exc).__name__}）]\n\n"
        yield from _demo_stream(messages)


TRIAGE_PROMPT = """你是「康伴」的健康分诊助手，根据用户提供的症状信息给出**初步参考建议**（绝不是诊断）。

请严格按以下 Markdown 结构输出，语言通俗：
1. **可能方向**：列出 2–4 种可能（一律用“可能/常见于”等措辞，不做确诊）。
2. **严重程度评估**：给出「轻微 / 中等 / 严重」的判断并简述理由。
3. **就医建议**：明确给出「居家观察 / 1–2 天内就医 / 尽快就医 / 立即急诊」四选一，并说明。
4. **注意事项**：居家护理要点，以及“出现哪些情况需立即就医”。

若信息中存在危及生命的紧急表现（剧烈胸痛、呼吸困难、大出血、意识丧失、中风征兆等），
就医建议必须为「立即急诊」，并置于最显眼位置。

结尾固定附一句：*以上分诊建议仅供参考，不能替代专业医生的诊断与治疗。*"""


def stream_triage(info: dict) -> Generator[str, None, None]:
    """基于结构化症状信息流式生成分诊建议。不可用时回退演示模式。"""
    user_prompt = _triage_user_prompt(info)
    if not is_configured():
        yield from _demo_triage_stream(info)
        return

    try:
        client = _build_client()
    except ImportError:
        yield from _demo_triage_stream(info)
        return

    payload = [
        {"role": "system", "content": TRIAGE_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=payload,
            stream=True,
            temperature=0.4,
            max_tokens=1200,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as exc:  # noqa: BLE001
        yield f"\n\n> :orange[（大模型调用失败，已切换为演示模式：{type(exc).__name__}）]\n\n"
        yield from _demo_triage_stream(info)


def _triage_user_prompt(info: dict) -> str:
    symptoms = "、".join(info.get("symptoms") or ["（未选择）"])
    extra = (info.get("extra") or "").strip()
    lines = [
        f"主要症状：{symptoms}",
        f"持续时间：{info.get('duration') or '未知'}",
        f"年龄段：{info.get('age') or '未知'}",
        f"主观严重程度：{info.get('severity') or '未填写'}",
    ]
    if extra:
        lines.append(f"补充描述：{extra}")
    return "\n".join(lines)


def _demo_triage_stream(info: dict) -> Generator[str, None, None]:
    reply = _demo_triage_reply(info)
    for i in range(0, len(reply), 3):
        yield reply[i : i + 3]
        time.sleep(0.01)


def _demo_triage_reply(info: dict) -> str:
    # 用 `or` 兜底：severity 可能为 None（用户未选择严重程度），
    # 若直接取默认值会落到「轻微 / 居家观察」，属于风险低估。
    severity = info.get("severity") or "中等"
    symptoms = "、".join(info.get("symptoms") or []) or "所述症状"

    if severity == "严重":
        advice = "尽快就医（或立即急诊）"
        level = "严重"
    elif severity == "中等":
        advice = "1–2 天内就医"
        level = "中等"
    else:
        advice = "居家观察"
        level = "轻微"

    return (
        f"根据你提供的信息（{symptoms}），初步参考如下：\n\n"
        "**1. 可能方向**\n"
        "- 常见于普通感染或炎症、疲劳等因素；\n"
        "- 也需排除其他功能性或慢性因素。\n\n"
        f"**2. 严重程度评估**：{level}\n\n"
        f"**3. 就医建议**：{advice}\n\n"
        "**4. 注意事项**\n"
        "- 注意休息、清淡饮食、多饮水，观察症状变化；\n"
        "- 若出现高热不退、呼吸困难、意识改变、剧烈疼痛等情况，请**立即就医**。\n\n"
        "（当前为演示模式，以上分诊建议仅供参考，不能替代专业医生的诊断与治疗。）"
    )


def _demo_stream(messages: list[dict]) -> Generator[str, None, None]:
    """内置演示回复：无 API Key 时也能流畅演示界面与交互。"""
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break

    reply = _demo_reply(last_user)
    # 模拟打字机效果，让演示更自然
    for i in range(0, len(reply), 3):
        yield reply[i : i + 3]
        time.sleep(0.01)


def _demo_reply(user_text: str) -> str:
    text = user_text or ""
    if any(k in text for k in ("感冒", "咳嗽", "发烧", "发热", "流鼻涕")):
        return (
            "听起来可能是普通的上呼吸道感染。建议：\n\n"
            "- 多喝温水、保证休息，避免熬夜；\n"
            "- 体温 <38.5℃ 可物理降温，超过可考虑退烧药（按说明书）；\n"
            "- 注意开窗通风，避免去人群密集处。\n\n"
            "如果高热超过 3 天、呼吸困难或症状明显加重，请及时就医。\n\n"
            "（以上为演示回复，仅供参考，不能替代专业诊疗。）"
        )
    if any(k in text for k in ("头痛", "头晕", "头疼")):
        return (
            "头痛原因较多，常见于疲劳、睡眠不足、压力或紧张性头痛。可先：\n\n"
            "- 保证充足睡眠、适当休息；\n"
            "- 减少屏幕时间，做适度放松；\n"
            "- 观察是否与姿势、情绪相关。\n\n"
            "若头痛突然剧烈发作、伴呕吐、发热、肢体无力或视物异常，请立即就医。\n\n"
            "（以上为演示回复，仅供参考。）"
        )
    if any(k in text for k in ("失眠", "睡不好", "睡眠")):
        return (
            "改善睡眠可以试试：\n\n"
            "- 固定作息，睡前 1 小时远离手机；\n"
            "- 白天适度运动，晚上避免咖啡、浓茶；\n"
            "- 睡前做放松或腹式呼吸。\n\n"
            "若长期失眠或打鼾伴呼吸暂停，建议就医评估。\n\n"
            "（以上为演示回复，仅供参考。）"
        )
    if any(k in text for k in ("血压", "高血压")):
        return (
            "高血压日常管理要点：\n\n"
            "- 低盐饮食（每日 <5g）、戒烟限酒、控制体重；\n"
            "- 规律运动、规律作息、保持情绪平稳；\n"
            "- 遵医嘱规律服药，**不要自行停药**，定期监测血压。\n\n"
            "若血压突然显著升高伴头痛、胸痛、视物模糊，请立即就医。\n\n"
            "（以上为演示回复，仅供参考。）"
        )
    return (
        "已收到你的问题。我是「康伴」健康问答助手，可以为你提供健康科普、症状参考、"
        "生活方式与慢病管理等方面的建议。\n\n"
        "⚠️ 需要提醒的是：我**不能替代医生**，无法给出诊断或处方。"
        "如果症状严重、持续或让你担忧，请及时到正规医疗机构就诊。\n\n"
        "（当前为演示模式——配置 DeepSeek API Key 后即可获得完整的智能回答。）"
    )
