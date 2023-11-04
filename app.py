import requests
from PIL import Image, ImageDraw, ImageFont
import openai
import streamlit as st
import json

# get_story takes the user input and gets a story from GPT.
# Example return data: {"title" : "title", "content", "content"}
def get_script_organize(script):
    with st.spinner('문학을 요약중입니다.'):
        try : 
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {"role":"system","content":"""
                     From now on, you are specialist that organizing this content. When the user inputs the lecture script, the input data must be organized according to the instructions below.
                     instructions : 
                     output
                     - 제목
                     - 목차
                     - 주제

                     ## 제목
                     1. 40자 내외 길이로 구성합니다.
                     2. 6개의 단어 이내로 정리합니다.
                     3. 구어체 혹은 대화체로 표현합니다.
                     4. 내용에 절차, 가짓수 표현이 여러번 반복되면 제목에 숫자를 사용합니다.
                     5. 일상어를 사용합니다.
                     6. 이익을 제시합니다.

                     ## 목차
                     1. 구어체 혹은 대화체로 표현합니다.
                     2. 일상어를 사용합니다.
                     3. 목차를 주제 or 키워드 or 시간의 순서 or 배경 or 분위기 기준으로 정리합니다.
                     4. 목차 전반 1/3

                     ## 주제
                     1. 목차에 따른 주제를 뽑아야 합니다
                     2. 하나의 목차에는 최소 1개의 주제, 최대 5개의 주제가 포함되어 있어야 합니다.
                     3. 구어체 혹은 대화체로 표현합니다.
                     4. 일상어를 사용합니다.

                     structure :
                     type : json
                     language : Korean
                     structure example : 
                     {"title":"title","contents":{"index":["subjects"],"index":["subjects","subjects"]}}"""},
                     {"role": "user","content": f"{script} 이 내용을 정리해줘"}
                ],
            )
            script = res["choices"][0]["message"]["content"]
        except openai.error.OpenAIError as e:
            print(e)
            st.error("OpenAI API로부터 컨텐츠 요약본을 얻는 동안 오류가 발생했습니다.")
            return None
        return script

openai.api_key = "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"

# Set the title of the web page.
st.title("📖 인문학 컨텐츠 요약 서비스")

# Create a form for the user to input the child's information.
with st.form(key='my_form'):
    st.write("인문학 컨텐츠를 입력해 주세요")
    script = st.text_input(label='컨텐츠')
    submit_button = st.form_submit_button(label='컨텐츠 요약하기')

# When the form is submitted, check the fields and display the story.
if submit_button:
    if not script:
        st.error("컨텐츠가 입력되지 않았습니다.")
    else:
        script = get_script_organize(script)
        st.write(script)