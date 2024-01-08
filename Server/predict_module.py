# 문장 분류 인공지능 모듈화

import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from sklearn.preprocessing import LabelEncoder
from konlpy.tag import Okt
import re

# model load
model = tf.keras.models.load_model('C:/Users/dargu/Desktop/jnu_whatsay/AI/recog_situation_model.h5')

def whatSayPredict(input_text):
    origin_text = input_text

    # 한국어 전처리 함수 정의
    def preprocess_korean_text(text):
        # 한국어 형태소 분석기 (KoNLPy)를 사용하여 토큰화
        okt = Okt()
        words = okt.morphs(text, stem=True)
        text = ' '.join(words)

        # 특수 문자, 숫자, 공백 제거
        text = re.sub(r'[^가-힣\s]', '', text)
        text = ' '.join(text.split())  # 중복 공백 제거

        # 불용어 제거
        stopwords = ['을', '를', '이', '가', '은', '는', '에서', '에게', '에', '로', '으로', '도', '한', '그', '고', '와', '듯', '듯이', '만', '밖에']
        tokens = text.split()
        tokens = [word for word in tokens if word not in stopwords]
        text = ' '.join(tokens)

        return text

    # 텍스트 열에 전처리 함수 적용
    input_text = preprocess_korean_text(input_text)

    # Tokenizing
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([input_text])

    input_sequence = tokenizer.texts_to_sequences([input_text])
    input_sequence = pad_sequences(input_sequence, maxlen=50)

    print("전처리 결과: " + input_text)

    # predict
    prediction = model.predict(input_sequence)
    print("predicted result:", prediction)

    for i in prediction:
        pre_ans = i.argmax()  # maximum class
    if pre_ans == 0: print("주제: 음식")
    if pre_ans == 1: print("주제: IT")
    if pre_ans == 2: print("주제: 학교 수업")
    if pre_ans == 3: print("주제: 운동")

    result = pre_ans

    return result