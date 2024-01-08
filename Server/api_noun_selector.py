import pandas as pd
import csv
from konlpy.tag import Okt

# 데이터 로드
data = pd.read_csv('C:/Users/dargu/Desktop/jnu_whatsay/AI/dataset.txt', sep=',', quoting=csv.QUOTE_NONE, encoding='utf-8')

okt = Okt()

# 클래스별 명사 배열 초기화
num_classes = data['label_column'].nunique()
noun_arrays = [[] for _ in range(num_classes)]

# 데이터 순회 및 명사 추출 함수
def extract_nouns(text):
    # 텍스트를 명사로 분석
    nouns = okt.nouns(text)
    
    # 불용어 처리
    stopwords = ['을', '를', '이', '가', '은', '는', '에서', '에게', '에', '로', '으로', '도', '한', '그', '고', '와', '듯', '듯이', '만', '밖에']
    nouns = [word for word in nouns if word not in stopwords]
    
    return nouns

# 데이터 순회하여 명사 배열 채우기
for index, row in data.iterrows():
    text = row['text_column']
    label = row['label_column']
    nouns = extract_nouns(text)
    noun_arrays[label].extend(nouns)

# 중복 단어 제거 함수
def remove_duplicates(arr):
    return list(set(arr))

# 클래스 번호를 입력하면 해당 클래스에 대한 명사 배열을 리턴하는 함수
def get_nouns_for_class(class_number):
    if class_number >= 0 and class_number < num_classes:
        nouns = noun_arrays[class_number]
        unique_nouns = remove_duplicates(nouns)
        return unique_nouns
    else:
        return []

# 테스트: 클래스 번호 0에 대한 중복 단어 제거된 명사 배열 가져오기
#class_0_nouns = get_nouns_for_class(0)
#print("Class 0 Nouns (Unique):", class_0_nouns)