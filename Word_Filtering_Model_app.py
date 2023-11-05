import time

import openai
import streamlit as st
from PIL import Image



openai.api_key = st.secrets["SECRET_KEY_GPT"]


# 함수들
def Apply_CSS_Style():
    # HTML에 CSS-STYLE 지정
    with open('style.css', encoding = "utf-8")as f:
        style = f.read()
    st.markdown(f"<style>{style}</style>", unsafe_allow_html = True)

def chat_GPT(User_question) :
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": User_question}
        ]
    )
    GPT_answer = completion.choices[0].message['content']
    return GPT_answer

def Loading():
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    return my_bar

Apply_CSS_Style()


User_question = st.chat_input(placeholder= "질문을 주시면 Chat-GPT가 답변합니다")

st.markdown(f'<p class="Hahmlet_Title">언어 감수성 분석</p>', unsafe_allow_html=True)
st.divider()

if User_question != None :
    user_message = st.chat_message("human", avatar="user")
    user_message.markdown(f'<p class="Hahmlet_Bold1">User</p>', unsafe_allow_html=True)
    user_message.write("")
    user_message.markdown(f'<p class="Hahmlet">{User_question}</p>', unsafe_allow_html=True)
    user_message.write("\n")

    # GPT의 답변
    gpt_message = st.chat_message("human", avatar = "ai")
    gpt_message.markdown(f'<p class="Hahmlet_Bold2">Chat-GPT</p>', unsafe_allow_html=True)
    gpt_message.write("")

    my_bar = Loading()
    # progress_text = "Operation in progress. Please wait."
    # my_bar = st.progress(0, text=progress_text)
    # for percent_complete in range(100):
    #     time.sleep(0.01)
    #     my_bar.progress(percent_complete + 1, text=progress_text)
    # time.sleep(1)

    GPT_answer = chat_GPT(User_question)

    if GPT_answer != None:
        my_bar.empty()
        gpt_message.markdown(f'<p class="Hahmlet">{GPT_answer}</p>', unsafe_allow_html=True)
        gpt_message.write("\n")


        my_bar = Loading()
        my_bar.empty()

        image = Image.open('./image/chat_bot_icon.jpg')
        filtered_message = st.chat_message("user", avatar = image)
        filtered_message.markdown(f'<p class="Hahmlet_Bold3">After Filtering</p>', unsafe_allow_html=True)
        filtered_message.write("")
        filtered_message.write("여기다가 결과를 씨부려~")
        filtered_message.markdown(f'<p class="Hahmlet">{GPT_answer}</p>', unsafe_allow_html=True)
        filtered_message.write("\n")

else :
    main_image = Image.open('./image/main.jpg')
    st.image(main_image)