import re

original_string = '"머신 러닝 모델은 신용 카드 거래를 감시하여 부정 거래를 탐지합니다"1\n"머신 러닝 모델은 신용 카드 거래를 감시하여 부정 거래를 탐지합니다"1\n"머신 러닝 모델은 신용 카드 거래를 감시하여 부정 거래를 탐지합니다"1\n"머신 러닝 모델은 신용 카드 거래를 감시하여 부정 거래를 탐지합니다"1'

# 정규 표현식을 사용하여 "내용" 다음에 오는 숫자를 찾아서 수정
result = re.sub(r'"(.*?)"(\d+)', r'"\1",\2', original_string)

# 결과 출력
print(result)
