# %%
import numpy as np
import pandas as pd
import csv
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# data load, preprocessing
data = pd.read_csv('./dataset.txt', sep = ",", quoting=csv.QUOTE_NONE, encoding='utf-8')
texts = data['text_column']
labels = data['label_column']


# %%
print("hi")

# %%
print("amount of datas : " + str(texts.count()))

amount_of_food = 0
amount_of_it = 0
amount_of_school = 0
amount_of_sports = 0

for i in labels:
    if i == 0:
        amount_of_food += 1
    elif i == 1:
        amount_of_it += 1
    elif i == 2:
        amount_of_school += 1
    elif i == 3:
        amount_of_sports += 1

print("food_data : " + str(amount_of_food) + "\nit_data : " + str(amount_of_it) + "\nschool_data : " + str(amount_of_school) + "\nsports_data : " + str(amount_of_sports))

# %%
from konlpy.tag import Okt

morpheme_sep = []

twt = Okt()

for i, j in enumerate(texts):
    tagging = twt.pos(texts[i])
    #print(str(tagging) + "\n")

    for k, h in tagging:
        morpheme_sep.append(k)

    stop_words = set(['은', '는', '이', '가', '하', '아', '것', '들','의', '있', '되', '수', '보', '주', '등', '한'])
    clean_data = [token for token in morpheme_sep if not token in stop_words]
    

print("not apply stop_words : " + str(morpheme_sep))
print("apply stop_words : " + str(clean_data))



# %%
print(texts[0])

# %%
# 한글 텍스트 형태소 분석
okt = Okt()
texts = texts.apply(lambda x: ' '.join(okt.morphs(x)))

tokenizer = Tokenizer(num_words=500)
tokenizer.fit_on_texts(texts)
X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X, maxlen=50)

# %%
print(texts[560])

# %%
print(labels)

# %%
import numpy as np

# NaN 또는 무한대 값을 가지는 인덱스 검사
nan_indices = np.where(np.isnan(labels))
inf_indices = np.where(np.isinf(labels))

print("NaN 값을 가지는 인덱스:", nan_indices)
print("무한대 값을 가지는 인덱스:", inf_indices)


# %%
# multiclass label prepare
from keras.utils import to_categorical

mean_value = labels.mean()
labels.fillna(mean_value, inplace=True)

# labels 배열을 정수로 변환
labels = labels.astype(int)
y = to_categorical(labels, num_classes=4)  # amount of class

# %%
print(text)

# %%
# data divising
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model structure
model = Sequential()
model.add(Embedding(input_dim=500, output_dim=64, input_length=50))
model.add(LSTM(4))
model.add(Dense(4, activation='softmax'))  # print softmax of 4 class

# compile
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# train
from keras.callbacks import EarlyStopping 
early_stopping = EarlyStopping(patience = 2) # protect overfitting

history = model.fit(X_train, y_train, epochs=20, batch_size=100, validation_split=0.2, verbose=1, callbacks = [early_stopping])
print(history.history)

# training visualizing (accuracy)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

#training visualizing (loss)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# evaluate
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Loss: {loss}, Accuracy: {accuracy}')

# model save
model.save('./recog_situation_model.h5')
print("학습된 모델이 저장되었습니다.")

# %%
model.summary()


