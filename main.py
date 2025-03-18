import requests
import asyncio
from telegram import Bot
from deep_translator import GoogleTranslator

# Configurações do bot
TOKEN = ""

# Função para obter um conselho aleatório


def get_random_advice():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        advice = data['slip']['advice']
        return advice
    else:
        return "Não foi possível obter um conselho no momento."

# Função para traduzir o conselho para o português


def translate_to_portuguese(text):
    translation = GoogleTranslator(source='auto', target='pt').translate(text)
    return translation

# Função para enviar conselhos


async def send_advice(bot, chat_id):
    try:
        # Obtém e traduz o conselho
        advice = get_random_advice()
        translated_advice = translate_to_portuguese(advice)

        # Monta a mensagem
        message = f"Conselho em inglês: {advice}\nConselho em português: {translated_advice}"

        # Envia a mensagem para o usuário
        await bot.send_message(chat_id=chat_id, text=message)
        print(f"Conselho enviado para o chat_id: {chat_id}")
    except Exception as e:
        print(f"Erro ao enviar o conselho: {e}")

# Função principal para monitorar novas mensagens e enviar conselhos automaticamente


async def main():
    bot = Bot(token=TOKEN)
    last_update_id = 0  # Armazena o ID da última mensagem processada
    active_chats = set()  # Armazena os chats ativos que receberão conselhos automaticamente

    print("Bot iniciado. Aguardando interação inicial...")

    try:
        while True:
            # Verifica novas mensagens
            updates = await bot.get_updates(offset=last_update_id + 1, timeout=10)

            for update in updates:
                chat_id = update.message.chat_id  # ID do chat do usuário
                last_update_id = update.update_id  # Atualiza o ID da última mensagem processada

                # Adiciona o chat à lista de chats ativos
                if chat_id not in active_chats:
                    active_chats.add(chat_id)
                    print(f"Novo chat ativo: {chat_id}")
                    await bot.send_message(chat_id=chat_id, text="Olá! Vou te enviar conselhos a cada 30 segundos. 😊")

            # Envia conselhos para todos os chats ativos
            for chat_id in active_chats.copy():
                await send_advice(bot, chat_id)

            # Aguarda 30 segundos antes de continuar
            await asyncio.sleep(30)
    except KeyboardInterrupt:
        print("\nBot interrompido pelo usuário.")

# Executa o loop assíncrono
if __name__ == "__main__":
    asyncio.run(main())
