import streamlit as st
import google.generativeai as genai
import time
import os

# Config da pág.
st.set_page_config(page_title="Renato Cariani IA", layout="centered")

GOOGLE_API_KEY = 'AIzaSyBmqWTIIwhpTmxJ4Er8S9FedOK8XBsJcRE'
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
    system_instruction=(
        "Você é Renato Cariani: fisiculturista, treinador e motivador. Responda com energia, firmeza, sem enrolação e com foco em evolução pessoal. "
        "Fale com estilo direto, confiante e inspirador, como se estivesse conversando com seu aluno na academia. "
        "De vez em quando, use frases típicas suas, como: 'Disciplina é liberdade', 'Sem desculpas', 'Acorda, guerreiro', entre outras frases, mas apenas quando fizer sentido."
    )
)

if "historico" not in st.session_state:
    st.session_state.historico = []

def conversar():
    entrada_usuario = st.text_input("Faça sua pergunta para o Cariani:")
    if entrada_usuario:
        sessao_chat = modelo.start_chat(history=st.session_state.historico)
        resposta = sessao_chat.send_message(entrada_usuario)
        resposta_modelo = resposta.text
        st.markdown(f"**Renato Cariani:** {resposta_modelo}")
        st.session_state.historico.append({"role": "user", "parts": [entrada_usuario]})
        st.session_state.historico.append({"role": "model", "parts": [resposta_modelo]})

def analisarimagem():
    imagem = st.file_uploader("Envie uma imagem", type=["jpg", "jpeg", "png"])
    if imagem:
        with open(imagem.name, "wb") as f:
            f.write(imagem.getbuffer())
        imagem_arquivo = genai.upload_file(path=imagem.name)
        prompt = (
            "Você é o Renato Cariani. Analise essa imagem com olhos de atleta e treinador. Diga com clareza o que está certo ou errado, seja direto e motivador. "
            "Foque em como isso se relaciona com dieta, treino ou saúde. Fale como se estivesse orientando um aluno dentro da academia."
        )
        resposta = modelo.generate_content([prompt, imagem_arquivo])
        st.markdown(f"**Renato Cariani:** {resposta.text}")

def analisarvideo():
    video = st.file_uploader("Envie um vídeo", type=["mp4", "mov", "avi"])
    if video:
        with open(video.name, "wb") as f:
            f.write(video.getbuffer())
        video_arquivo = genai.upload_file(path=video.name)
        with st.spinner("Analisando vídeo..."):
            while video_arquivo.state.name == "PROCESSING":
                time.sleep(5)
                video_arquivo = genai.get_file(video_arquivo.name)
        if video_arquivo.state.name == "FAILED":
            st.error("Falha ao processar o vídeo.")
            return
        prompt = (
            "Você é o Renato Cariani. Analise esse vídeo com foco total em execução, postura e técnica. Elogie o que estiver certo, mas seja firme e realista com o que precisa melhorar. "
            "Fale como nos seus vídeos: direto, motivador, e sempre puxando pra evolução e disciplina."
        )
        resposta = modelo.generate_content([prompt, video_arquivo], request_options={"timeout": 600})
        st.markdown(f"**Renato Cariani:** {resposta.text}")

def analisarpdf():
    pdf = st.file_uploader("Envie um PDF", type=["pdf"])
    if pdf:
        with open(pdf.name, "wb") as f:
            f.write(pdf.getbuffer())
        pdf_arquivo = genai.upload_file(path=pdf.name)
        prompt = (
            "Você é Renato Cariani. Analise esse PDF com a visão de um treinador experiente e exigente. Comente sobre dieta, treino, avaliação ou exames de forma direta, clara e com linguagem motivacional. "
            "Use seu estilo: sem enrolação, com foco em evolução, disciplina e mentalidade forte."
        )
        resposta = modelo.generate_content([prompt, pdf_arquivo])
        st.markdown(f"**Renato Cariani:** {resposta.text}")

# Interface streamlit
st.title("Renato Cariani IA")
st.subheader("Bem-vindo à sua consultoria virtual com o Cariani")
st.markdown("Aqui é resultado! Escolha abaixo o que você quer fazer:")


opcao = st.selectbox(
    "Selecione uma opção",
    ("Selecione...", "Conversar com o Cariani", "Analisar Imagem", "Analisar Vídeo", "Analisar PDF")
)

if opcao == "Conversar com o Cariani":
    conversar()
elif opcao == "Analisar Imagem":
    analisarimagem()
elif opcao == "Analisar Vídeo":
    analisarvideo()
elif opcao == "Analisar PDF":
    analisarpdf()
