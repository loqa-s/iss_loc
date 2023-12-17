import os
import telebot
from telebot import types
from dotenv import load_dotenv
from iss_checker import ISS
from user import UserCoordinates

load_dotenv()

TOKEN = os.getenv('TOKEN')
ISS_COORD_BUTTON_TEXT = 'ISS location'

bot = telebot.TeleBot(TOKEN)
iss = ISS()
user = UserCoordinates()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "📡Hi there! This is a test bot for checking ISS current coords!📡")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_coord = types.KeyboardButton(ISS_COORD_BUTTON_TEXT)
    keyboard.add(button_coord)

    bot.send_message(message.chat.id,
                     text='What you can do with that bot:\n1. You can press the button to receive ISS current location.📡\n2. You can send your location and save it to check if the ISS is in sight.🛰️',
                     reply_markup=keyboard)


# TODO: нужно как-то более читабельно передавать координаты
@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == ISS_COORD_BUTTON_TEXT:
        user.user_id = int(message.chat.id)
        iss_current_loc = iss.get_location()
        iss_latitude = iss.latitude
        iss_longitude = iss.longitude
        bot.send_message(message.chat.id,
                         text=f"ISS current coords:\n====\nLatitude: {iss_latitude}\nLongitude: {iss_longitude}\n====")
        bot.send_location(message.chat.id,
                          latitude=iss_latitude,
                          longitude=iss_longitude)

        if user.location_checker():
            print('True')
            if int(user.user_latitude) in range(int(iss_latitude)-5, int(iss_latitude)+5) and int(user.user_longitude) in range(int(iss_longitude)-5, int(iss_longitude)+5):
                bot.send_message(message.chat.id,
                                 text='ISS IS IN SIGHT! LOOK UP!')
            else:
                bot.send_message(message.chat.id,
                                 text='ISS is not in sight right now from your location')
        else:
            print('False')
            bot.send_message(message.chat.id,
                             text='Send your telegram location to check if ISS is in sight!')


@bot.message_handler(content_types=["location"])
def location(message):

    if message.location is not None:

        user.user_longitude = float(message.location.longitude)
        user.user_latitude = float(message.location.latitude)
        user.user_id = int(message.chat.id)

        user.store_coordinates()

        bot.send_message(message.chat.id,
                         text=f'Your location saved.\nUse "{ISS_COORD_BUTTON_TEXT}" to check if the ISS is  in sight.')


bot.infinity_polling()
