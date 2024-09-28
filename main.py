import os
import telebot
from openai import OpenAI

client = OpenAI(api_key="")
# Utilizați variabile de mediu pentru chei și token-uri
bot = telebot.TeleBot('7825844128:AAHovUmmPb3En8CmiE4Z0m-vKWajFwdOc2Y')


def chat_with_gpt(prompt):
    response = client.chat.completions.create(model="gpt-4",  # Poți folosi și gpt-3.5-turbo pentru un cost mai mic
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    # Returnează răspunsul generat
    return response.choices[0].message.content

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f'Bună ziua, {message.from_user.first_name}, compania StarNet te salută, cu ce te putem ajuta?')

@bot.message_handler()
def start(message):
    response = chat_with_gpt(message.text.lower())
    bot.send_message(message.chat.id, response)

if __name__ == "__main__":
    bot.polling(none_stop=True)