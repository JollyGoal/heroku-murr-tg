import json
import os
import time

import requests
import telebot

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

queue_array = []

minutes = 1


def process_kick_step(message):
    chat_id = message.chat.id
    global minutes
    global queue_array
    # print("Kick step activated")
    try:
        a = 0
        while a <= minutes:
            # print(a)
            time.sleep(10)  # TODO
            a += 1
        if len(queue_array) != 0:
            for i in range(len(queue_array)):
                if queue_array[i] == message.new_chat_member.id:
                    # print("Ban this man!!!!")
                    bot.send_message(message.chat.id, f'User have been kicked {message.new_chat_member.first_name}')
                    # print(queue_array[i])
                    queue_array.pop(i)
                    # print(queue_array)
                    r = requests.get(
                        f'https://api.telegram.org/bot1071519299:AAHaBlATLsQ5THcU-j-I6g8xZnpLjJSdC1M/kickChatMember?chat_id={message.chat.id}&user_id={message.new_chat_member.id}')

                    user_data = json.loads(r.text)
                    print(user_data)
    except:
        pass


@bot.message_handler(content_types=["text"])
def check_users(message):
    global queue_array
    # print('Message received')
    chat_id = message.chat.id
    if len(queue_array) != 0:
        for i in range(len(queue_array)):
            if queue_array[i] == message.from_user.id:
                queue_array.pop(i)
                bot.send_message(message.chat.id, f'Checked! {message.from_user.first_name}')
                # print("He has been removed from queue")
    else:
        bot.reply_to(message, 'I am still working (Это сообщение будет только в DEBUG моде)')


@bot.message_handler(content_types=["new_chat_members"])
def send_welcome(message):
    global queue_array
    global minutes
    chat_id = message.chat.id
    if not message.new_chat_member.is_bot:
        text = f"Здарова, <b>{message.new_chat_member.first_name}</b>! Расскажи чем интересуешься и что хочешь найти в Мурренган? Если не напишешь в течение {minutes} минут, тебе грозит <b>КИК</b> из группы 😁"
        bot.reply_to(message, text, parse_mode="HTML")
        queue_array.append(message.new_chat_member.id)
        # print(queue_array)
        # print(message)
        process_kick_step(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
