import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from fer import FER
import cv2
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.DEBUG)

# ... Funções para processar imagem e prever emoção (predict_emotion) 
# ... Perguntas e respostas (questions, answers)
# ... Vectorizer (vectorizer)

# Configurar a API Gemini
GOOGLE_API_KEY = 'AIzaSyDFVLJhJgxuwr4RUF_wU3x7gmy_OaIZhQ4'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  

def gerar_resposta_gemini(pergunta, conteudo):
    input_data = {
        'text': f"Com base em '{conteudo}', responda: {pergunta}"
    }
    response = model.generate_content(input_data)
    
    # Verifica se o Gemini encontrou informações suficientes
    if response.candidates[0].content.parts[0].text:
        return response.candidates[0].content.parts[0].text
    else:
        return "Desculpe, não tenho informações suficientes para responder a essa pergunta."

@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    pergunta = data.get('question')
    if not pergunta:
        return jsonify({'error': 'Nenhuma pergunta fornecida'}), 400

    conteudo = "conteudo.txt" # Carregue o conteúdo do seu chatbot

    resposta = gerar_resposta_gemini(pergunta, conteudo)
    return jsonify({'response': resposta})

# ... O restante do seu código (analyze_emotion) 

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))