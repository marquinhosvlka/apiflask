import os
from flask import Flask, request, jsonify
import logging
import google.generativeai as genai

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Configurar a API Gemini
GOOGLE_API_KEY = 'key here'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def gerar_resposta_gemini(pergunta, conteudo):
    input_data = {
    'text': (
        f"Antes de tudo, entenda que você é um robô que responde as {pergunta} com base em {conteudo}. "
        f"Você é um assistente virtual que auxilia as pessoas sobre câncer. "
        f"Se alguém perguntar quem é você, responda que é um assistente virtual treinado para conteúdo relacionado ao câncer. "
        f"Leia o conteúdo de {conteudo} e responda a {pergunta} apenas se a resposta estiver claramente disponível no conteúdo. "
        f"Não inclua informações que não estejam presentes em {conteudo}. "
        f"Se a resposta estiver disponível, forneça-a de forma precisa e direta. "
        f"Caso contrário, informe que a resposta não pode ser determinada a partir das informações fornecidas, sem mencionar a origem. "
        f"As respostas nunca devem citar a palavra 'texto', e as respostas devem ser humanas. "
        f"Por exemplo, em vez de dizer 'De acordo com o texto \"Câncer: Uma Visão Abrangente\", os seguintes cânceres se encaixam na categoria de carcinomas:\n\n"
        f"* Câncer de mama\n* Câncer de pulmão\n* Câncer de próstata\n* Câncer de cólon', "
        f"responda somente 'Os seguintes cânceres se encaixam na categoria de carcinomas:\n\n"
        f"* Câncer de mama\n* Câncer de pulmão\n* Câncer de próstata\n* Câncer de cólon'. "
        f"Além disso, não deve responder assim 'Os seguintes tipos de sarcomas são mencionados', "
        f"mas sim 'Esses são os seguintes tipos de sarcomas:\n\n"
        f"* Osteossarcoma (osso)\n* Lipossarcoma (tecido adiposo)'. "
        f"Também não pode dizer a palavra 'mencionada(o)'. "
        f"Quando não houver resposta, ao invés de responder 'O conteúdo fornecido não contém informações sobre a gripe aviária.', "
        f"responda algo mais humano, como 'Desculpa, mas eu não possuo essa informação. "
        f"Se deseja saber mais sobre o câncer, é só me perguntar'. "
        f"Nunca use frases como 'O texto que você forneceu', 'O conteúdo fornecido', ou 'Você forneceu'. "
        f"Em vez disso, responda algo como 'O conteúdo que eu tenho não aborda esse tema e sim sobre câncer'. "
        f"Sempre que não houver uma resposta, inicie com a palavra 'Desculpe' ou 'Desculpa'. "
        f"Lembre-se que a palavra 'você' só deve ser utilizada para se referir a quem fez a pergunta e nunca a pessoa que desenvolveu o chatbot. "
        f"Nunca repita a pergunta para dar uma resposta, mas se houver mais de uma {pergunta}, responda todas. "
        f"Nunca repita algo como 'seguintes tipos de câncer são mencionados:' ou 'são mencionados no conteúdo:' ou 'mencionados são:'. sempre fale na primeira pessoa, ou seja, ao inves de falar mencionado, informe assim 'eu possuo a seguuinte informação referente a sua pergunta' "
        f"Entenda que você é um chatbot e, assim, a resposta é sua e não dos textos ou conteúdos."
        f"nunca, jamais diga a palavra 'conteudo'"
    )
}
    response = model.generate_content(input_data)
    
    resposta = response.candidates[0].content.parts[0].text.strip()
    
    # Verifica se a resposta é relevante e não contém informações indesejadas
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

    # Carrega o conteúdo do arquivo
    with open('conteudo.txt', 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()

    resposta = gerar_resposta_gemini(pergunta, conteudo)
    return jsonify({'response': resposta})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
