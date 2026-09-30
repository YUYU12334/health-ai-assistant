"""康伴 · AI 个人健康问答助手 —— 应用入口。

技术栈：Streamlit + DeepSeek（OpenAI 兼容接口），未配置 API Key 时自动回退演示模式。
"""

from __future__ import annotations

import streamlit as st

from utils import deepseek

st.set_page_config(
    page_title="康伴 · AI 个人健康问答助手",
    page_icon=":material/health_and_safety:",
    layout="centered",
    initial_sidebar_state="auto",
)

# 共享会话状态：跨页面的对话历史
st.session_state.setdefault("messages", [])

pages = [
    st.Page("app_pages/chat.py", title="智能问答", icon=":material/chat:", default=True),
    st.Page("app_pages/triage.py", title="症状分诊", icon=":material/clinical_notes:"),
    st.Page("app_pages/knowledge.py", title="健康知识库", icon=":material/menu_book:"),
    st.Page("app_pages/about.py", title="安全与免责", icon=":material/shield:"),
]

page = st.navigation(pages, position="top")

# 侧边栏：品牌、连接状态、全局操作
with st.sidebar:
    st.title("康伴")
    st.caption("AI 个人健康问答助手")

    if deepseek.is_configured():
        st.success("已连接 DeepSeek 大模型", icon=":material/check_circle:")
    else:
        st.warning(
            "演示模式 · 未配置 API Key\n\n在 `.streamlit/secrets.toml` 填入 `DEEPSEEK_API_KEY` 后即可启用完整智能问答。",
            icon=":material/info:",
        )

    if st.button("清空对话记录", icon=":material/delete:", width="stretch"):
        st.session_state.messages = []
        st.rerun()

    st.caption("本产品仅提供健康科普与参考建议，不构成医疗建议；紧急情况请拨打 120。")

# 顶部常驻安全提示（所有页面可见）
st.caption(":material/info: 本助手提供健康科普与参考建议，**不能替代专业医生诊断与治疗**；如遇紧急情况请立即拨打 **120**。")

page.run()
