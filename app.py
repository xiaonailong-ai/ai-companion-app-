import streamlit as st
from openai import OpenAI
import os

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="C:/Users/fjxzj/Downloads/emoji_1781080249593.svg",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 初始化 session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "name" not in st.session_state:
    st.session_state.name = "小奶龙"
if "xg" not in st.session_state:
    st.session_state.xg = "小奶龙是一个特别可爱小AI助手"

# 侧边栏
with st.sidebar:
    st.subheader("伴侣信息")
    st.text_input("名字", value="小奶龙", key="name")   # 自动绑定
    st.text_area("性格", value="小奶龙是一个特别可爱小AI助手", key="xg")

st.title("AI智能伴侣")

# 显示历史消息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

system_prompt = f"你的名字叫{st.session_state.name}，{st.session_state.xg}"
prompt = st.chat_input("请输入要问的问题")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_message.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
