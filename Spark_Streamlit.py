import streamlit as st
import SparkApi

st.set_page_config(page_title="星火大模型3.5", layout="centered", page_icon="🔥")

#以下密钥信息从控制台获取
appid = "your appid"   
api_secret = "your api_secret" 
api_key ="your api_key" 

#用于配置大模型版本
domain = "generalv3.5"

#云端环境的服务地址
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"  # v3.0环境的地址

text =[]
def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if __name__ == '__main__':
    st.success("欢迎与星火大模型3.5进行交流")
    user_input = st.chat_input("请输入你计划咨询的问题，按回车键提交！")
    if user_input is not None:
        progress_bar = st.empty()
        with st.spinner("内容已提交，星火大模型3.5模型正在作答中！"):
            question = checklen(getText("user", user_input))
            SparkApi.answer = ""
            SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
            feedback = getText("assistant", SparkApi.answer)[1]["content"]
            if feedback:
                progress_bar.progress(100)
                st.session_state['chat_history'].append((user_input, feedback))
                for i in range(len(st.session_state["chat_history"])):
                    user_info = st.chat_message("user")
                    user_content = st.session_state["chat_history"][i][0]
                    user_info.write(user_content)

                    assistant_info = st.chat_message("assistant")
                    assistant_content = st.session_state["chat_history"][i][1]
                    assistant_info.write(assistant_content)

                with st.sidebar:
                    if st.sidebar.button("清除对话历史"):
                        st.session_state["chat_history"] = []

            else:
                st.info("对不起，我回答不了这个问题，请你更换一个问题，谢谢！")