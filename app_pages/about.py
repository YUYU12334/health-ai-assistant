"""安全与免责说明页。"""

from __future__ import annotations

import streamlit as st

from utils import deepseek

st.header("安全与免责", icon=":material/shield:", anchor=False)
st.caption("使用前请阅读以下说明。健康无小事，我们始终把安全放在第一位。")

with st.container(border=True):
    st.markdown("### ⚠️ 重要免责声明")
    st.markdown(
        """
「康伴」是一款基于人工智能技术的**健康科普与参考建议工具**，仅用于健康知识普及和一般性健康管理参考。

1. **不构成医疗建议**：本产品提供的所有内容均**不能替代**执业医师的诊断、治疗、处方或专业医疗意见。
2. **不提供诊断与处方**：本产品不会（也不应被理解为）对任何疾病作出确诊或开具用药方案。
3. **请及时就医**：如有任何身体不适，尤其是症状持续、加重或让你担忧时，请务必到正规医疗机构就诊。
4. **信息时效性**：医学知识不断更新，本产品内容可能存在滞后，请以专业医生意见为准。

*使用本产品即表示你已理解并同意上述内容。*
        """
    )

with st.container(border=True):
    st.markdown("### 🚑 紧急情况指引")
    st.markdown(
        """
如出现以下**任一**情况，请**立即拨打 120 急救电话**或前往最近急诊，不要等待 AI 回复：

- 剧烈或压榨性胸痛、胸闷，伴出汗、恶心
- 呼吸困难、窒息感、嘴唇发紫
- 大量出血、吐血、咯血
- 突然意识丧失、昏迷、抽搐
- 一侧肢体无力、口角歪斜、言语不清（中风征兆）
- 严重外伤、骨折、烧烫伤、中毒、溺水、触电
        """
    )
    st.caption("急救电话：120 ｜ 火警：119 ｜ 报警：110")

with st.container(border=True):
    st.markdown("### 💙 心理健康支持")
    st.markdown(
        """
如果你正在经历情绪困扰或有自伤想法，请**立即联系可信任的人**，或拨打以下援助热线：

- 全国统一心理援助热线：**12356**
- 希望24热线：**400-161-9995**
- 青少年心理援助热线：**12355**
        """
    )

with st.container(border=True):
    st.markdown("### 🛠️ 关于本作品")
    st.markdown(
        """
- **作品名称**：康伴 · AI 个人健康问答助手
- **赛道**：软件赛道（医药健康 · AI 个人健康问答助手）
- **技术栈**：Streamlit + DeepSeek 大模型（OpenAI 兼容接口）
- **功能模块**：智能问答对话、症状自查/分诊、健康知识库、问答历史、安全护栏与免责声明

**安全设计说明**：本产品内置紧急症状识别与心理危机识别，在检测到相关表述时会优先引导用户拨打急救电话或求助热线，而不是由 AI 给出常规建议，从而降低误导风险。
        """
    )

    if deepseek.is_configured():
        st.success("当前已连接 DeepSeek 大模型", icon=":material/check_circle:")
    else:
        st.warning(
            "当前为演示模式。在 `.streamlit/secrets.toml` 中填入 `DEEPSEEK_API_KEY` 即可启用完整智能问答。",
            icon=":material/info:",
        )

st.caption("康伴 · AI 个人健康问答助手 ｜ 仅供健康科普与参考，不构成医疗建议")
