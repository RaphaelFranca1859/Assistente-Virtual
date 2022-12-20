import speech_recognition as sr
from nltk import word_tokenize, corpus
import json
import webbrowser as web

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "Assistente-Virtual-main\config.json"


def iniciar():
    global reconhecedor
    global palavras_de_parada
    global nome_assistente
    global acoes

    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))

    with open(CAMINHO_CONFIGURACAO, "r", encoding = 'utf8') as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)

        nome_assistente = configuracao["nome"]
        acoes = configuracao["acoes"]

        arquivo_configuracao.close()


def escutar_comando():
    global reconhecedor
    
    comando = None
    
    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)
        
        print("Ana: Fale alguma coisa...")        
        fala = reconhecedor.listen(fonte_audio, timeout=5, phrase_time_limit=5)
        try:
            comando = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        except sr.UnknownValueError:
            pass
    
    return comando
    


def eliminar_palavras_de_parada(tokens):
    global palavras_de_parada
    
    tokens_filtrados = []
    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)
    
    return tokens_filtrados


def tokenizar_comando(comando):
    global nome_assistente
    
    acao = None
    objeto = None
    
    tokens = word_tokenize(comando, IDIOMA_CORPUS)
    if tokens:
        tokens = eliminar_palavras_de_parada(tokens)
        
        if len(tokens) >= 3:
            if nome_assistente == tokens[0].lower():
                acao = tokens[1].lower()
                objeto = tokens[2].lower()            
    
    return acao, objeto
    

def validar_comando(acao, objeto):
    global acoes
    
    valido = False
    
    if acao and objeto:
        for acaoCadastrada in acoes:
            if acao == acaoCadastrada["nome"]:
                if objeto in acaoCadastrada["objetos"]:
                    valido = True
                    
                break
    
    return valido


def executar_comando(acao, objeto):
    print("Ana: vou executar o comando:", acao, objeto)



if __name__ == '__main__':
    iniciar()

    continuar = True
    while continuar:
        try:
            comando = escutar_comando()
            print(f"Ana: processando o comando: {comando}")

            if comando == "Ana Abrir Gmail":
                web.open('https://mail.google.com/mail/u/0/#inbox')
            if comando == "Ana Abrir Google":
                web.open('https://www.google.com.br')
            if comando == "Ana Abrir agenda":
                web.open('https://calendar.google.com/calendar/u/0/r?tab=wc')
        
            if comando:
                acao, objeto = tokenizar_comando(comando)
                valido = validar_comando(acao, objeto)
                if valido:
                    executar_comando(acao, objeto)
                else:
                    print("Ana: Não entendi o comando. Repita, por favor!")
        except KeyboardInterrupt:
            print("Ana: Tchau!")

            continuar = False


