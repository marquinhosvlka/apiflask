from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from fer import FER
import cv2
import tensorflow

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Função para processar a imagem e prever a emoção
def predict_emotion(image_path):
    try:
        # Carregar a imagem
        img = cv2.imread(image_path)
        if img is None:
            return 'Error: Image not found or unable to load image'

        # Criar o detector de emoções
        detector = FER()

        # Detectar emoções
        result = detector.detect_emotions(img)
        if not result:
            return 'unknown'

        # Obter a emoção dominante
        emotions = result[0]['emotions']
        if not emotions:
            return 'unknown'

        dominant_emotion = max(emotions, key=emotions.get)
        return dominant_emotion
    except Exception as e:
        return f'Error during prediction: {str(e)}'

questions = [
    "O que é câncer?",
    "Quais são os tipos de câncer mais comuns?",
    "Quais são os sintomas do câncer de mama?",
    "Quais são os sintomas do câncer de pulmão?",
    "Quais são os sintomas do câncer de próstata?",
    "Quais são os sintomas do câncer de cólon?",
    "Quais são os fatores de risco para câncer?",
    "Como é feito o diagnóstico de câncer?",
    "Quais são os tratamentos disponíveis para câncer?",
    "Como a quimioterapia trata o câncer?",
    "Como a radioterapia trata o câncer?",
    "O que é imunoterapia?",
    "O que são terapias alvo?",
    "Como prevenir o câncer?",
    "Qual a importância do diagnóstico precoce do câncer?",
    "Boa noite",
    "Bom dia",
    "Boa tarde",
    "Olá",
    "Oi",
    "Tudo bem?",
    "Como você está?",
    "Obrigado",
    "Tchau",
    "O câncer tem cura?",
    "Como saber se estou curado do câncer?",
    "O que acontece depois que o câncer é curado?",
    "Como saber se eu tenho câncer?"
]

answers = [
    "Câncer é uma doença caracterizada pelo crescimento descontrolado de células anormais no corpo.",
    "Os tipos de câncer mais comuns incluem câncer de mama, pulmão, próstata e cólon.",
    "Os sintomas do câncer de mama podem incluir um caroço na mama, mudanças no tamanho ou forma da mama, e secreção pelo mamilo.",
    "Os sintomas do câncer de pulmão podem incluir tosse persistente, dor no peito, falta de ar e perda de peso inexplicável.",
    "Os sintomas do câncer de próstata podem incluir dificuldade para urinar, fluxo urinário fraco, sangue na urina e dor pélvica.",
    "Os sintomas do câncer de cólon podem incluir mudanças nos hábitos intestinais, sangue nas fezes, dor abdominal e perda de peso inexplicável.",
    "Fatores de risco para câncer incluem tabagismo, exposição a radiação, dieta pobre, falta de atividade física e predisposição genética.",
    "O diagnóstico de câncer pode ser feito através de exames como biópsias, tomografias, ressonâncias magnéticas e exames de sangue.",
    "Os tratamentos para câncer incluem cirurgia, radioterapia, quimioterapia, imunoterapia e terapias alvo.",
    "A quimioterapia trata o câncer usando medicamentos que matam células cancerosas ou impedem seu crescimento.",
    "A radioterapia usa radiação de alta energia para matar células cancerosas ou impedir seu crescimento.",
    "A imunoterapia estimula o sistema imunológico do corpo para combater o câncer.",
    "Terapias alvo são tratamentos que atacam especificamente as células cancerosas sem afetar muito as células normais.",
    "Para prevenir o câncer, recomenda-se evitar o tabagismo, manter uma dieta saudável, praticar atividade física regular, e fazer exames regulares de rastreamento.",
    "O diagnóstico precoce do câncer é importante porque aumenta as chances de sucesso do tratamento e pode salvar vidas.",
    "Boa noite, tudo bem?",
    "Bom dia! Como posso ajudar você hoje?",
    "Boa tarde! Em que posso ser útil?",
    "Olá! Como posso te ajudar hoje?",
    "Oi! Precisa de alguma informação?",
    "Estou bem, obrigado! E você?",
    "Estou bem, obrigado por perguntar! E você?",
    "De nada! Como posso ajudar mais?",
    "Tchau! Tenha um bom dia!",
    "Sim, muitos tipos de câncer têm cura, especialmente se diagnosticados precocemente e tratados adequadamente.",
    "Para saber se está curado do câncer, é necessário acompanhamento médico e exames regulares para verificar se o câncer não retornou.",
    "Depois que o câncer é curado, o paciente precisa continuar com acompanhamento médico regular para monitorar a saúde e prevenir possíveis recidivas.",
    "Para saber se você tem câncer, é importante consultar um médico, que pode solicitar exames como biópsias, tomografias, ressonâncias magnéticas e exames de sangue com base nos sintomas e histórico médico."
]

vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(questions).toarray()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    question_vector = vectorizer.transform([question]).toarray()
    similarity = cosine_similarity(question_vector, vectors)
    index = np.argmax(similarity)
    response = answers[index]
    return jsonify({'response': response})

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Prever a emoção
            emotion = predict_emotion(file_path)
            return jsonify({'dominant_emotion': emotion})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'File processing error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
