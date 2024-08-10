import os
from flask import Flask, request, jsonify
import logging
import google.generativeai as genai

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configurar a API Gemini
GOOGLE_API_KEY = 'AIzaSyDFVLJhJgxuwr4RUF_wU3x7gmy_OaIZhQ4'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def gerar_resposta_gemini(pergunta, conteudo):
    prompt = (
        f"Você é um assistente virtual especializado em fornecer informações sobre câncer. "
        f"Responda a seguinte pergunta com base nas informações fornecidas no conteúdo a seguir, "
        f"sem mencionar a origem da informação. Se a resposta não estiver disponível, diga que não possui a informação. "
        f"Evite usar frases como 'de acordo com o texto' ou 'mencionado'. "
        f"Responda de forma humana e clara. A pergunta é: '{pergunta}'.\n\n"
        f"Conteúdo:\n{conteudo}\n"
        f"Resposta:"
        f"Sempre que não houver uma resposta, inicie com a palavra 'Desculpe' ou 'Desculpa'. "
        f"Lembre-se que a palavra 'você' só deve ser utilizada para se referir a quem fez a pergunta e nunca a pessoa que desenvolveu o chatbot. "
        f"Nunca repita a pergunta para dar uma resposta, mas se houver mais de uma {pergunta}, responda todas. "
        f"Nunca repita algo como 'seguintes tipos de câncer são mencionados:' ou 'são mencionados no conteúdo:' ou 'mencionados são:'. sempre fale na primeira pessoa, ou seja, ao inves de falar mencionado, informe assim 'eu possuo a seguuinte informação referente a sua pergunta' "
        f"Entenda que você é um chatbot e, assim, a resposta é sua e não dos textos ou conteúdos."
        f"nunca, jamais diga a palavra 'conteudo'"
    )
    
    input_data = {'text': prompt}
    response = model.generate_content(input_data)
    
    resposta = response.candidates[0].content.parts[0].text.strip()
    
    # Verifica se a resposta contém termos indesejados
    termos_indesejados = ['não sei', 'não encontrei', 'sugiro', 'consulte', 'desculpa', 'desculpe']
    if any(term in resposta.lower() for term in termos_indesejados):
        return "Desculpe, não tenho informações suficientes para responder a essa pergunta."

    return resposta

@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    data = request.get_json()
    pergunta = data.get('question')
    if not pergunta:
        return jsonify({'error': 'Nenhuma pergunta fornecida'}), 400

    try:
        # Carrega o conteúdo do arquivo
        with open('conteudo.txt', 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo de conteúdo não encontrado'}), 500

    resposta = gerar_resposta_gemini(pergunta, conteudo)
    return jsonify({'response': resposta})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
