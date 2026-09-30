"""内置健康知识库（常见健康主题 FAQ）。

这些内容仅用于科普与演示，不构成医疗建议。真实项目中可替换为
数据库或向量检索的知识库。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthTopic:
    category: str
    title: str
    question: str
    answer: str


HEALTH_TOPICS: tuple[HealthTopic, ...] = (
    HealthTopic(
        category="常见症状",
        title="普通感冒与流感怎么区分",
        question="普通感冒和流感有什么区别？",
        answer=(
            "普通感冒起病较缓，症状以鼻塞、流涕、咽痛为主，发热较轻或没有；"
            "流感起病急，常伴高热（39℃以上）、明显乏力、肌肉酸痛和头痛。"
            "流感更易引起肺炎等并发症，高危人群（老人、儿童、孕妇、慢性病患者）应及早就医。"
        ),
    ),
    HealthTopic(
        category="常见症状",
        title="发热了怎么办",
        question="发烧了应该怎么处理？",
        answer=(
            "体温低于 38.5℃ 且精神尚可时，可多饮水、物理降温、注意休息。"
            "超过 38.5℃ 可考虑使用解热镇痛药（如对乙酰氨基酚或布洛芬，按说明书、避免重复用药）。"
            "若持续高热超过 3 天、伴有意识改变、呼吸困难、皮疹或婴幼儿发热，请及时就医。"
        ),
    ),
    HealthTopic(
        category="常见症状",
        title="头痛的常见原因",
        question="经常头痛是怎么回事？",
        answer=(
            "头痛原因很多，常见的有紧张性头痛（压力、疲劳、姿势不良）、偏头痛（搏动性、可伴恶心畏光）、"
            "睡眠不足或咖啡因戒断等。若头痛突然剧烈发作（“雷击样”）、伴发热、颈强直、肢体无力或意识改变，"
            "需立即就医排查严重病因。反复或影响生活的头痛应到神经内科就诊。"
        ),
    ),
    HealthTopic(
        category="慢病管理",
        title="高血压日常注意什么",
        question="高血压患者日常生活要注意什么？",
        answer=(
            "低盐饮食（每日食盐 <5g）、戒烟限酒、控制体重、规律运动（每周 ≥150 分钟中等强度）、"
            "保证睡眠、减轻精神压力。遵医嘱规律服药，**不要自行停药或调药**，并定期监测血压、复诊。"
            "若血压突然显著升高伴头痛、胸痛、视物模糊，需立即就医。"
        ),
    ),
    HealthTopic(
        category="慢病管理",
        title="糖尿病饮食原则",
        question="糖尿病人应该怎么吃？",
        answer=(
            "控制总热量，定时定量；主食粗细搭配，减少精制糖和含糖饮料；"
            "多吃蔬菜，适量优质蛋白（鱼、禽、蛋、豆制品），限制高脂肪食物；"
            "水果选择低升糖指数的，放在两餐之间少量食用。具体方案应结合血糖监测与营养科/内分泌科医生建议。"
        ),
    ),
    HealthTopic(
        category="生活方式",
        title="成年人每天睡多久合适",
        question="成年人每天睡多久比较合适？",
        answer=(
            "多数成年人建议每晚 7–9 小时。长期少于 6 小时或睡眠质量差会增加肥胖、心血管疾病和情绪问题的风险。"
            "保持规律作息、睡前减少屏幕与咖啡因、营造安静黑暗的睡眠环境有助于改善睡眠。"
            "若长期失眠或打鼾伴呼吸暂停，建议就医评估。"
        ),
    ),
    HealthTopic(
        category="生活方式",
        title="健康成年人每周运动量",
        question="健康成年人每周应该运动多少？",
        answer=(
            "建议每周至少 150 分钟中等强度有氧运动（如快走、骑车、游泳），或 75 分钟高强度运动，"
            "并配合每周 2 次以上力量训练。循序渐进，避免突然剧烈运动；有心肺疾病或长期不运动者，开始前可先咨询医生。"
        ),
    ),
    HealthTopic(
        category="心理健康",
        title="如何缓解焦虑情绪",
        question="压力大、焦虑怎么办？",
        answer=(
            "可以尝试规律作息、适度运动、腹式呼吸或正念放松；把担忧写下来、与信任的人倾诉也有帮助。"
            "若焦虑持续、明显影响工作生活，或伴心慌、失眠、情绪低落，建议寻求心理咨询或精神科医生的专业帮助。"
        ),
    ),
    HealthTopic(
        category="用药安全",
        title="药品可以混着吃吗",
        question="感冒药和退烧药能一起吃吗？",
        answer=(
            "许多复方感冒药已含有解热镇痛成分（如对乙酰氨基酚），再叠加退烧药容易**过量**，损伤肝脏。"
            "服药前务必阅读说明书，核对成分，避免重复用药；不确定时应咨询药师或医生。"
            "处方药请严格遵医嘱。"
        ),
    ),
)

CATEGORIES: tuple[str, ...] = tuple(
    dict.fromkeys(t.category for t in HEALTH_TOPICS)
)


def search_topics(query: str) -> list[HealthTopic]:
    """按关键词在标题与问题中检索，返回匹配的话题列表。"""
    q = query.strip()
    if not q:
        return list(HEALTH_TOPICS)
    return [
        t for t in HEALTH_TOPICS
        if q in t.title or q in t.question or q in t.answer
    ]
