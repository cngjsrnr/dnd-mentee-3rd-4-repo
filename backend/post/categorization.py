from tensorflow.python.keras.preprocessing import sequence
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.models import model_from_json
from eunjeon import Mecab #이걸 은전한잎말고 konlpy꺼로 쓰면 정확도 80퍼 넘음
import os

# 형태소 분류
def tokenize_data(data):
    mecab = Mecab()
    tag_classes = ['NNG', 'NNP', 'VA', 'VV+EC',
                   'XSV+EP', 'XSV+EF', 'XSV+EC', 'VV+ETM']
    i = 0

    speech_pos = mecab.pos(data)
    data = [n for n, tag in speech_pos if tag in tag_classes]
    return data


# 데이터 전처리
def x_pretreatment(X):
    max_word = 5000  # 많이 사용된 단어 몇개쓸지
    max_len = 500  # 길이제한(뉴스마다 길이가 다르니 고정 빈부분은 0으로 채움)

    tok = Tokenizer(num_words=max_word)
    tok.fit_on_texts(X)  # 각 단어에 번호를 부여
    # print(len(tok.word_index))
    # print(tok.word_index)

    sequences = tok.texts_to_sequences(X)  # 부여한 번호로 시퀀스화시킴
    # print(len(sequences[0]))
    # print(sequences[0])

    sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_len)  # 벡터화
    # print(sequences_matrix)
    # print(sequences_matrix[0])
    # print(len(sequences_matrix[0]))
    return sequences_matrix


# str형태의 data를 받아옴(뉴스본문)
def Categorization(data):
    category=["경제","국제","문화","사회","스포츠","취미","연예","정치","IT&과학","라이프"]

    module_dir = os.path.dirname(__file__)
    model_path = os.path.join(module_dir, 'categorization_model.json')
    weight_path = os.path.join(module_dir, 'best_model.h5')

    # 학습모델 불러옴
    json_file = open(model_path, "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(weight_path)

    # 모델 컴파일
    loaded_model.compile(loss='categorical_crossentropy',
                         optimizer='adam',
                         metrics=['accuracy'])

    # 형태소 분류
    content = tokenize_data(data)

    # 데이터 전처리
    sequences_matrix = x_pretreatment([content])


    answer = loaded_model.predict_classes(sequences_matrix)
    return category[answer[0]]
