from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

OPENAI_API_URL = "https://hekchat-openai.openai.azure.com/openai/deployments/model-gpt-35-turbo-16k/chat/completions?api-version=2023-07-01-preview"
#OPENAI_API_URL = "https://hekchat-openai.openai.azure.com//chat/completions"
YOUR_OPENAI_API_KEY = "e0a5da9b62fa47cd991976f68c0e9521"

@app.route('/', methods=['GET'])
def index():  
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # リクエストからユーザーの入力メッセージを取得
    user_message = request.json['message']

    # OpenAI APIへのリクエストパラメータを設定
    payload = {
        "prompt": user_message,
        "max_tokens": 50
    }

#    # プロキシの設定
#    proxies = {
#    "http": "http://sera:Ej3AR1MH,<@172.16.1.23:15080",
#    "https": "http://sera:Ej3AR1MH,<@172.16.1.23:15080"
#    }

    headers={
        "Content-Type": "application/json",
        "api-key": YOUR_OPENAI_API_KEY
    }


    try:
        # OpenAI APIにリクエストを送信
        response = requests.post(
            OPENAI_API_URL,
            headers=headers,
            data=json.dumps(payload)
#            data=json.dumps(payload),
#            proxies=proxies  # プロキシを指定
        )

        # レスポンスから生成されたテキストを取得
        generated_text = response.json()["choices"][0]["message"]["content"]

        # レスポンスを返す
        return jsonify({'message': generated_text})

    except Exception as e:
        # エラーメッセージを返す
        print("error:",e)
        return jsonify({'message': 'エラーが発生しましたよ。'})
#        return jsonify({'message': e})

if __name__ == '__main__':
    app.run(debug=True)
