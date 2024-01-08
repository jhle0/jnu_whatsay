from flask import Flask, request, make_response, jsonify  # Flask에서 jsonify를 가져옵니다.
from flask import request

import json
from flask import make_response

# 자연어 처리 문장 예측 모듈
from predict_module import whatSayPredict
from api_noun_selector import get_nouns_for_class

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/')
def home():
    return 'JNU_Whatsay natural language processing API server.'

# /predtext로 쓰면 404오류가 뜸. /predtext/로 이슈 해결
@app.route('/predtext/', methods=['GET'])
def predict_text():
    input_text = request.args.get('text')

    print("입력값: " + input_text)

    pred_class = whatSayPredict(input_text)
    pred_class = int(pred_class)
    #noun_collect = get_nouns_for_class(pred_class)

    result = pred_class
    return jsonify(result)

@app.route('/getnoun/', methods=['GET'])
def get_noun():
    sel_class = request.args.get('class')
    sel_class = int(sel_class)
    result = get_nouns_for_class(sel_class)
    result = json.dumps(result, ensure_ascii=False)
    res = make_response(result)

    return res

if __name__ == '__main__':
    app.run(port=5000, debug=True)