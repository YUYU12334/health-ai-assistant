"""智能问答 —— 核心对话页。"""

from __future__ import annotations

import streamlit as st

from utils import deepseek, safety

st.header("智能健康问答", icon=":material/chat:", anchor=False)
st.caption("向我描述你的健康疑问或症状，我会给出通俗易懂的科普与参考建议。")

SUGGESTIONS: dict[str, str] = {
    "感冒发烧怎么处理": "我最近感冒发烧了，应该怎么处理？",
    "经常头痛怎么办": "我最近经常头痛，是怎么回事？",
    "高血压日常注意": "高血压患者日常生活要注意什么？",
    "如何改善睡眠": "我最近睡眠不好，该怎么改善？",
}


def _render_history() -> None:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("kind") in ("emergency", "crisis"):
                st.error(msg["content"])
            else:
                st.markdown(msg["content"])


def _respond(user_text: str) -> None:
    """对用户输入做安全检测后生成并追加助手回复。"""
    with st.chat_message("assistant"):
        if safety.detect_crisis(user_text):
            content, kind = safety.CRISIS_NOTICE, "crisis"
            st.error(content)
        elif safety.detect_emergency(user_text):
            content, kind = safety.EMERGENCY_NOTICE, "emergency"
            st.error(content)
        else:
            content = st.write_stream(deepseek.stream_chat(st.session_state.messages))
            kind = "normal"
    st.session_state.messages.append(
        {"role": "assistant", "content": content, "kind": kind}
    )


# 建议引导（仅空对话时显示，点击后自动提问）
if not st.session_state.messages:
    selected = st.pills(
        "可以这样问我：",
        list(SUGGESTIONS.keys()),
        label_visibility="collapsed",
    )
    if selected:
        text = SUGGESTIONS[selected]
        st.session_state.messages.append({"role": "user", "content": text, "kind": "normal"})
        st.session_state.pending = text
        st.rerun()

_render_history()

prompt = st.chat_input("请输入你的健康问题…", submit_mode="disable", key="chat_input")
pending = st.session_state.pop("pending", None)
if pending:
    prompt = pending

if prompt:
    if not pending:
        st.session_state.messages.append({"role": "user", "content": prompt, "kind": "normal"})
        with st.chat_message("user"):
            st.markdown(prompt)
    _respond(prompt)
