from flask import Flask, request, jsonify, render_template
#import os
from openai import AzureOpenAI

app = Flask(__name__)

#os.environ["http_proxy"] = "http://sera:Ej3AR1MH,<@172.16.1.23:15080"
#os.environ["https_proxy"] = "http://sera:Ej3AR1MH,<@172.16.1.23:15080"

client = AzureOpenAI(
    api_key="e0a5da9b62fa47cd991976f68c0e9521",
    api_version="2023-07-01-preview",
    azure_endpoint = "https://hekchat-openai.openai.azure.com/"
    )

deployment_name='model-gpt-35-turbo-2'


@app.route('/', methods=['GET'])
def index():  
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # リクエストからユーザーの入力メッセージを取得
    user_message = request.json['message']

    try:
        # OpenAI APIにリクエストを送信
        response = client.completions.create(
            model=deployment_name
          , prompt=user_message
          , max_tokens=100
        )

        # レスポンスから生成されたテキストを取得
        generated_text = response.choices[0].text
        print("generated_text:",generated_text)

        # レスポンスを返す
        return jsonify({'message': generated_text})

    except Exception as e:
        # エラーメッセージを返す
        print("error:",e)
        return jsonify({'message': 'エラーが発生しましたよ。'})

if __name__ == '__main__':
    app.run(debug=True)
