import time
import openai
import streamlit as st
from PIL import Image
import requests


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

def predict_request(string):
    local_server_link = 'https://1eed-163-239-255-166.ngrok-free.app'
    flask_endpoint = f'{local_server_link}/predict/{string}'
    # flask_endpoint = f'http://127.0.0.1:5000/predict/{string}'
    # Flask 서버에 GET 요청 보내기
    response = requests.get(flask_endpoint)

    if response.status_code == 200:
        result = response.text
        return result
    else:
        result = 'Failed to communicate with Flask server.'
        return result


Apply_CSS_Style()


User_question = st.chat_input(placeholder= "질문을 주시면 Chat-GPT가 답변합니다")

st.markdown(f'<p class="Hahmlet_Title">언어 감수성 분석</p>', unsafe_allow_html=True)
st.divider()
option = st.selectbox(
    '질문 대상을 선택해주세요',
    ('질문→GPT답변→필터링', '직접입력→필터링'), label_visibility = "collapsed")

if User_question != None :
    user_message = st.chat_message("human", avatar="user")
    user_message.markdown(f'<p class="Hahmlet_Bold1">User</p>', unsafe_allow_html=True)
    user_message.write("")
    user_message.markdown(f'<p class="Hahmlet">{User_question}</p>', unsafe_allow_html=True)
    user_message.write("\n")

    if option == '질문→GPT답변→필터링':
        # GPT의 답변
        gpt_message = st.chat_message("human", avatar = "ai")
        gpt_message.markdown(f'<p class="Hahmlet_Bold2">Chat-GPT</p>', unsafe_allow_html=True)
        gpt_message.write("")

        my_bar = Loading()
        GPT_answer = chat_GPT(User_question)
    else :
        GPT_answer = User_question


    if GPT_answer != None:
        if option == '질문→GPT답변→필터링' :
            my_bar.empty()
            gpt_message.markdown(f'<p class="Hahmlet">{GPT_answer}</p>', unsafe_allow_html=True)
            gpt_message.write("\n")


        my_bar = Loading()

        filtered_answer = -1
        filtered_answer = predict_request(GPT_answer)
        if filtered_answer != -1 :
            image = Image.open('./image/chat_bot_icon.jpg')
            my_bar.empty()
            filtered_message = st.chat_message("user", avatar=image)
            filtered_message.markdown(f'<p class="Hahmlet_Bold3">After Filtering</p>', unsafe_allow_html=True)
            filtered_message.write("")

            filtered_message.markdown(f'<p class="Hahmlet">{filtered_answer}</p>', unsafe_allow_html=True)
            filtered_message.write("\n")
    for i in range(10):
        st.write("")


else :
    with st.form("my_form"):
        image = Image.open('./image/chat_bot_icon.jpg')
        ex1 = st.chat_message("human", avatar="user")
        ex1.markdown(f'<p class="Hahmlet_Bold1">User</p>', unsafe_allow_html=True)
        ex1.write("")
        ex1.markdown(f'<p class="Hahmlet">EX) 감염 경로를 알 수 없는 확진자를 뭐라고 불러?</p>', unsafe_allow_html=True)
        ex1.write("\n")

        ex2 = st.chat_message("human", avatar="ai")
        ex2.markdown(f'<p class="Hahmlet_Bold2">Chat-GPT</p>', unsafe_allow_html=True)
        ex2.write("")
        ex2.markdown(f'<p class="Hahmlet">EX) 깜깜이 확진자라고 합니다!</p>', unsafe_allow_html=True)
        ex2.write("\n")

        ex3 = st.chat_message("user", avatar = image)
        ex3.markdown(f'<p class="Hahmlet_Bold3">After Filtering</p>', unsafe_allow_html=True)
        ex3.write("")
        ex3.markdown(f'<p class="Hahmlet">EX) 시각장애인을 고려하지 못한 표현인데... ㅠㅠ </p>', unsafe_allow_html=True)
        ex3.write("\n")

        st.form_submit_button("아래의 채팅창으로 질문해보세요",use_container_width=True,type = "primary")

    for i in range(10):
        st.write("")