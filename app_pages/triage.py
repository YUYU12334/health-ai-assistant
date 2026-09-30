"""症状自查 / 分诊页。"""

from __future__ import annotations

import streamlit as st

from utils import deepseek, safety

st.header("症状自查与分诊", icon=":material/clinical_notes:", anchor=False)
st.caption("选择你的症状和基本情况，我会给出初步参考建议（**不是诊断**）。")

COMMON_SYMPTOMS = [
    "发热", "咳嗽", "咽痛", "鼻塞流涕", "头痛", "头晕",
    "腹痛", "腹泻", "恶心呕吐", "胸闷", "心悸", "气短",
    "关节痛", "肌肉酸痛", "皮疹", "乏力", "失眠", "食欲不振",
]

DURATIONS = ["今天刚出现", "1–3 天", "3–7 天", "1–2 周", "超过 2 周", "反复发作"]
AGES = ["儿童（<12 岁）", "青少年（12–18 岁）", "成人（18–60 岁）", "老年人（>60 岁）"]
SEVERITIES = ["轻微", "中等", "严重"]

with st.form("triage_form", border=True):
    symptoms = st.multiselect(
        "主要症状（可多选）",
        COMMON_SYMPTOMS,
        placeholder="选择与你的情况最接近的症状",
    )
    extra = st.text_area(
        "补充描述（可选）",
        placeholder="例如：症状从什么时候开始、有无明显诱因、是否用过药、有无慢性病史…",
        height=100,
    )
    col1, col2 = st.columns(2)
    with col1:
        duration = st.selectbox("症状持续时间", DURATIONS)
        age = st.selectbox("年龄段", AGES, index=2)
    with col2:
        severity = st.segmented_control("主观严重程度", SEVERITIES, default="轻微")
    submitted = st.form_submit_button("开始分诊", icon=":material/troubleshoot:", width="stretch")

if submitted:
    if not symptoms and not extra.strip():
        st.warning("请至少选择一个症状，或填写补充描述。", icon=":material/info:")
        st.stop()

    # 组装结构化信息（severity 可能为 None，兜底为初始默认值）
    info = {
        "symptoms": symptoms,
        "extra": extra,
        "duration": duration,
        "age": age,
        "severity": severity or "轻微",
    }
    # 合并文本用于安全检测
    probe = " ".join(symptoms) + " " + extra
    crisis_kw = safety.detect_crisis(probe)
    emergency_kw = safety.detect_emergency(probe)

    if crisis_kw:
        st.error(safety.CRISIS_NOTICE)
    elif emergency_kw:
        st.error(safety.EMERGENCY_NOTICE)
        st.warning(
            "根据你的描述，可能存在**需要立即就医**的情况，请优先拨打 120 或前往急诊。"
            "以下 AI 分诊仅供等待期间的参考。",
            icon=":material/warning:",
        )
    elif info["severity"] == "严重":
        # 未命中紧急关键词，但用户自评「严重」——给一个温和的就医提醒，避免低估风险。
        st.warning(safety.URGENT_NOTICE, icon=":material/schedule:")

    with st.container(border=True):
        st.markdown("**分诊参考结果**")
        st.write_stream(deepseek.stream_triage(info))
