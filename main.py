import os
import telebot
import openai
# Utilizați variabile de mediu pentru chei și token-uri
bot = telebot.TeleBot('')
openai.api_key = ""


def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Poți folosi și gpt-3.5-turbo pentru un cost mai mic
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Returnează răspunsul generat
    return response['choices'][0]['message']['content']

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f'Bună ziua, {message.from_user.first_name}, compania StarNet te salută, cu ce te putem ajuta?')

@bot.message_handler()
def start(message):
    response = chat_with_gpt(message.text.lower())
    bot.send_message(message.chat.id, response)

if __name__ == "__main__":
    bot.polling(none_stop=True)