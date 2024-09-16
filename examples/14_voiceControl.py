from flask import Flask, jsonify, render_template, request, send_file
import openai
import requests
import os
import re
from gtts import gTTS
from io import BytesIO

app = Flask(__name__)

# OpenAI API 키를 환경 변수에서 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# ChatGPT API 호출 함수
def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Maru, a friendly pet robot named 강GPT. Your role is to assist and interact with your owner, 정현우. Be polite, helpful, and respectful."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            n=1,
            temperature=0.6,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error with ChatGPT API: {str(e)}"

# Flask 라우트
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    recognized_text = data.get('command', '').lower()

    # 1. 인식된 명령어를 로봇 제어 앱에 전달
    command_map = {
        "앞으로가": "forward",
        "뒤로가": "backward",
        "오른쪽으로 돌아": "left",
        "왼쪽으로 돌아": "right",
        "멈춰": "stop"
    }

    action = command_map.get(recognized_text, None)
    if action:
        try:
            # 로봇 제어 앱에 POST 요청 보내기
            response = requests.post('http://localhost:5001/control', data={'action': action})
            return jsonify({"recognized": recognized_text, "response": f"Executed: {action}"})
        except requests.exceptions.RequestException as e:
            return jsonify({"recognized": recognized_text, "response": f"Error sending command to robot: {str(e)}"})
    else:
        # ChatGPT를 통해 답변을 얻음
        chatgpt_response = get_chatgpt_response(f"정현우님이 요청하신 명령어 '{recognized_text}'에 대한 답변을 제공해 주세요.")
        
        # gTTS를 사용하여 응답을 음성으로 변환
        tts = gTTS(text=chatgpt_response, lang='ko')
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        
        return send_file(audio_file, mimetype='audio/mpeg', as_attachment=True, download_name='response.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
