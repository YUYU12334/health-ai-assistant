"""健康知识库 + 问答历史页。"""

from __future__ import annotations

import streamlit as st

from utils.knowledge_base import CATEGORIES, HEALTH_TOPICS, search_topics

st.header("健康知识库", icon=":material/menu_book:", anchor=False)
st.caption("浏览常见健康主题，或查看你本次对话的历史记录。")

tab_kb, tab_history = st.tabs(["健康知识库", "问答历史"])

# ---------- 健康知识库 ----------
with tab_kb:
    col1, col2 = st.columns([3, 2])
    with col1:
        query = st.text_input(
            "搜索健康主题",
            placeholder="输入关键词，如：感冒、高血压、睡眠…",
            label_visibility="collapsed",
        )
    with col2:
        category = st.selectbox("按分类筛选", ["全部"] + list(CATEGORIES))

    results = search_topics(query)
    if category != "全部":
        results = [t for t in results if t.category == category]

    st.caption(f"共 {len(results)} 条相关主题")

    if not results:
        st.info("没有找到匹配的主题，试试其他关键词。", icon=":material/search_off:")

    for i, topic in enumerate(results):
        with st.expander(f"{topic.title}  ·  {topic.category}"):
            st.markdown(f"**{topic.question}**")
            st.markdown(topic.answer)
            if st.button(
                "带着这个问题去问答页",
                key=f"ask_{i}",
                icon=":material/arrow_forward:",
            ):
                st.session_state.pending = topic.question
                st.switch_page("app_pages/chat.py")

# ---------- 问答历史 ----------
with tab_history:
    messages = st.session_state.get("messages", [])
    if not messages:
        st.info("暂无对话记录，去「智能问答」页开始提问吧。", icon=":material/chat:")
    else:
        top_left, top_right = st.columns([2, 1], vertical_alignment="center")
        with top_left:
            st.caption(f"本次会话共 {len(messages)} 条消息")
        with top_right:
            history_text = "\n\n".join(
                f"【{'用户' if m['role'] == 'user' else '助手'}】\n{m['content']}"
                for m in messages
            )
            st.download_button(
                "导出对话",
                data=history_text,
                file_name="康伴对话记录.txt",
                mime="text/plain",
                icon=":material/download:",
                width="stretch",
            )

        for i, m in enumerate(messages):
            with st.chat_message(m["role"]):
                if m.get("kind") in ("emergency", "crisis"):
                    st.error(m["content"])
                else:
                    st.markdown(m["content"])
