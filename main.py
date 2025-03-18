import requests
import time
from googletrans import Translator


def get_random_advice():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        advice = data['slip']['advice']
        return advice
    else:
        return "Não foi possível obter um conselho no momento."


def translate_to_portuguese(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='pt')
    return translation.text


def main():
    print("Iniciando o loop de conselhos. Pressione Ctrl + C para parar.")

    try:
        while True:
            # Obtém e traduz o conselho
            advice = get_random_advice()
            translated_advice = translate_to_portuguese(advice)

            # Exibe o conselho
            print("\nConselho em inglês:", advice)
            print("Conselho em português:", translated_advice)

            # Aguarda 30 segundos antes de continuar
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nLoop interrompido pelo usuário.")


if __name__ == "__main__":
    main()
