import time
import re

# 데이터 전처리
path = input("데이터셋의 경로를 입력해주세요 : ")
data = open(path, "r", encoding="UTF8")
print("데이터를 불러왔습니다.")
texts = data.read().replace("text_column,label_calumn", "")
print(texts + "\n\n")
print("데이터 수 : " + str(texts.count(",")) + "\n\n")
time.sleep(1)

print("[Process 1]\n이중 공백을 제거합니다.")
print("발견된 이중 공백 : " + str(texts.count("  ")))
texts = texts.replace("  ", "")
print("제거 완료\n\n")
time.sleep(0.5)

print("[Process 2]\n쉼표와 인덱스 사이의 공백을 제거합니다.")
print("발견된 공백 : " + str(texts.count(", 0") + texts.count(", 1") + texts.count(", 2") + texts.count(", 3")))
texts = texts.replace(", 0", ",0").replace(", 1", ",1").replace(", 2", ",2").replace(", 3", ",3")
print("제거 완료\n\n")
time.sleep(0.5)

print("[Process 3]\n불필요한 줄넘김을 제거합니다.")
print("발견된 줄넘김 : " + str(texts.count("\n\n")))
texts = texts.replace("\n\n", "\n")
print("제거 완료\n\n")
time.sleep(0.5)

print("[Process 4]\n모든 쉼표를 제거합니다.")
texts = texts.replace(",", "")
print("제거 완료\n\n")
time.sleep(0.5)

print("[Process 5]\n적절한 위치에만 쉼표를 재삽입합니다.")
texts = texts.replace("text_columnlabel_column", "text_column,label_column")
texts = re.sub(r'"(.*?)"(\d+)', r'"\1",\2', texts)
print("생성 완료\n\n")
time.sleep(0.5)

print("[Process 6]\n중복되는 데이터를 제거합니다.")
lines = texts.split('\n')
unique_lines = list(set(lines))
texts = '\n'.join(unique_lines)
print("제거 완료\n\n")
time.sleep(0.5)

print("[Process 7]\n데이터를 클래스 별로 묶어 재정렬합니다.")
# 데이터셋을 줄 단위로 분할
lines = texts.split('\n')

# 첫 번째 줄에서 헤더(컬럼 이름)를 추출
header = lines[0]
lines = lines[1:]

# 데이터를 클래스(라벨)에 따라 그룹화하고 정렬
label_groups = {}
for line in lines:
    parts = line.split(',')
    if len(parts) >= 2:
        label = int(parts[-1])  # 라벨은 마지막 열에 있다고 가정하며 숫자로 변환
        if label in label_groups:
            label_groups[label].append(line)
        else:
            label_groups[label] = [line]

# 라벨 순서대로 데이터를 정렬
sorted_lines = []
for label in sorted(label_groups.keys()):
    sorted_lines.extend(sorted(label_groups[label]))

# 정렬된 데이터에 헤더를 다시 추가
sorted_lines.insert(0, header)

# 정렬된 데이터를 문자열로 결합
texts = '\n'.join(sorted_lines)
print("재정렬 완료\n\n")
time.sleep(0.5)

print("\n\n수정된 데이터를 파일에 저장합니다.")
print("새로운 파일을 만들어 저장합니다.\n파일명 : processed_dataset.txt")
data.close()
data = open("./processed_dataset.txt", "w", encoding="UTF8")
data.write(texts)
data.close()
print("모든 작업이 완료되었습니다.\n")
print("수동으로 체크해야 할 사항\n1. 데이터의 클래스와 클래스 번호가 일치하는지 확인.\n2. 데이터에 쌍따옴표가 없는 데이터가 있는지 확인.")
