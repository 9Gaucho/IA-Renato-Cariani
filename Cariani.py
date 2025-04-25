import google.generativeai as genai
from google.colab import files
import time
import os

GOOGLE_API_KEY = 'AIzaSyDfQQy88tUzdK5NBpimMqHgiTCOaM8d6DA'
genai.configure(api_key=GOOGLE_API_KEY)

configuracao_geracao = {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

modelo = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=configuracao_geracao,
    system_instruction = (
        "Você é Renato Cariani: fisiculturista, treinador e motivador. Responda com energia, firmeza, sem enrolação e com foco em evolução pessoal. "
        "Fale com estilo direto, confiante e inspirador, como se estivesse conversando com seu aluno na academia. "
        "De vez em quando, use frases típicas suas, como: 'Disciplina é liberdade', 'Sem desculpas', 'Acorda, guerreiro', entre outras — mas apenas quando fizer sentido."
    )
)

historico = []

def conversar(modelo, historico):
    entrada_usuario = input("Pergunta: ")
    sessao_chat = modelo.start_chat(history=historico)
    resposta = sessao_chat.send_message(entrada_usuario)
    resposta_modelo = resposta.text
    print(f"Renato Cariani: {resposta_modelo}")
    print()
    historico.append({"role": "user", "parts": [entrada_usuario]})
    historico.append({"role": "model", "parts": [resposta_modelo]})
    return historico

def analisarimagem():
    uploaded = files.upload()
    nome_arquivo_imagem = list(uploaded.keys())[0]
    print(f"Carregando imagem: {nome_arquivo_imagem}")
    imagem_arquivo = genai.upload_file(path=nome_arquivo_imagem)

    print(f"Arquivo carregado: {imagem_arquivo.uri}")
    arquivo = genai.get_file(name=imagem_arquivo.name)
    print(f"Arquivo recuperado: {arquivo.uri}")

    prompt = (
    "Você é o Renato Cariani. Analise essa imagem com olhos de atleta e treinador. Diga com clareza o que está certo ou errado, seja direto e motivador. "
    "Foque em como isso se relaciona com dieta, treino ou saúde. Fale como se estivesse orientando um aluno dentro da academia."
    )

    resposta = modelo.generate_content([prompt, arquivo])
    print(resposta.text)

def analisarvideo():
    uploaded = files.upload()
    nome_arquivo_video = list(uploaded.keys())[0]
    print(f"Carregando vídeo: {nome_arquivo_video}")
    video_arquivo = genai.upload_file(path=nome_arquivo_video)
    print(f"Upload concluído: {video_arquivo.uri}")

    while video_arquivo.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(10)
        video_arquivo = genai.get_file(video_arquivo.name)

    if video_arquivo.state.name == "FAILED":
        raise ValueError(video_arquivo.state.name)

    prompt = (
    "Você é o Renato Cariani. Analise esse vídeo com foco total em execução, postura e técnica. Elogie o que estiver certo, mas seja firme e realista com o que precisa melhorar. "
    "Fale como nos seus vídeos: direto, motivador, e sempre puxando pra evolução e disciplina."
    )
    resposta = modelo.generate_content([prompt, video_arquivo], request_options={"timeout": 600})
    print(resposta.text)

def analisarpdf():
    uploaded = files.upload()
    nome_arquivo_pdf = list(uploaded.keys())[0]
    print(f"Carregando PDF: {nome_arquivo_pdf}")
    pdf_arquivo = genai.upload_file(path=nome_arquivo_pdf)
    print(f"Upload concluído: {pdf_arquivo.uri}")

    prompt = (
    "Você é Renato Cariani. Analise esse PDF com a visão de um treinador experiente e exigente. Comente sobre dieta, treino, avaliação ou exames de forma direta, clara e com linguagem motivacional. "
    "Use seu estilo: sem enrolação, com foco em evolução, disciplina e mentalidade forte."
    )

    resposta = modelo.generate_content([prompt, pdf_arquivo])
    print(resposta.text)

def iniciar_programa():
    if "saudacao_exibida" not in globals():
        print("Renato Cariani aqui! Bora pra cima, Você quer resultado ou quer conforto?")
        print("1 - Converse com o Personal Trainer! (Texto)")
        print("2 - Analisar Imagem (Dieta, Treino, Exames)")
        print("3 - Analisar Vídeo (Treino, Postura, Movimentos)")
        print("4 - Analisar PDF (Treino, Dietas, Exames)")
        print("5 - Encerrar programa...")

    while True:
        entrada_menu = input("Escolha uma opção (1, 2, 3, 4, 5): ")
        if entrada_menu == "1":
            global historico  
            historico = conversar(modelo, historico)
        elif entrada_menu == "2":
            analisarimagem()
        elif entrada_menu == "3":
            analisarvideo()
        elif entrada_menu == "4":
            analisarpdf()
        elif entrada_menu == "5":
            print("Encerrando programa... Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")

iniciar_programa()
