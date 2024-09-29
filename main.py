import os
import telebot
from telebot import types
from openai import OpenAI
from dotenv import load_dotenv
import speedtest


load_dotenv()

client = OpenAI(api_key= os.getenv('OPENAI_TOKEN'))
# Utilizați variabile de mediu pentru chei și token-uri
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))


def chat_with_gpt(prompt):
    response = client.chat.completions.create(model="gpt-4",  # Poți folosi și gpt-3.5-turbo pentru un cost mai mic
    messages=[
        {"role": "system", "content": "Salut tu esti assistent tehnic la compania StarNet. Incearca sa rezolvi problemele clientiilor, in caz ca clientul intreaba viteza la internet returneaza doar cuvantul 'speed' si nimic alt ceva, daca clientul intreaba date de balanta returneaza balanta fiind egala cu o cifra de la 100 la 2000, cifra de la zecimale mereu e 0, daca spui ca are nevoie de consultarea tehnicealui trimite si numarul de telefon 022 844 444, in caz ca clientul este agresiv, foloseste cuvinte necenzurate trimite ! in fata raspunsului "},
        {"role": "user", "content": prompt}
    ])

    # Returnează răspunsul generat
    return response.choices[0].message.content


def check_internet_speed():
    st = speedtest.Speedtest()
    # Get best server based on ping
    st.get_best_server()

    # Perform download and upload speed tests
    download_speed = st.download() / 1_000_000  # Convert from bits per second to Megabits per second
    upload_speed = st.upload() / 1_000_000      # Convert from bits per second to Megabits per second

    # Get ping (latency)
    ping = st.results.ping

    return [round(download_speed, 2), round(upload_speed, 2), round(ping, 2)]


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f'Bună ziua, {message.from_user.first_name}, compania StarNet te salută, cu ce te putem ajuta?')

@bot.message_handler(commands=['speed'])
def speed_test(message):
    bot.send_message(message.chat.id, 'Viteza dumnevoastra la internet(poate dura pana la 10 sec testarea):')
    speed = check_internet_speed()
    result = f'Viteza de descarcare {speed[0]}  mb/s Viteza de incarcare {speed[1]} mb/s  Ping {speed[2]} ms'
    bot.send_message(message.chat.id, result)

@bot.message_handler()
def start(message):
    response = chat_with_gpt(message.text.lower())
    if response.lower() != 'speed':
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, 'Viteza dumnevoastra la internet(poate dura pana la 10 sec testarea):')
        speed = check_internet_speed()
        result = f'Viteza de descarcare {speed[0]} \n mb/s Viteza de incarcare {speed[1]} mb/s \n Ping {speed[2]} ms'
        bot.send_message(message.chat.id, result)

if __name__ == "__main__":
    bot.polling(none_stop=True)