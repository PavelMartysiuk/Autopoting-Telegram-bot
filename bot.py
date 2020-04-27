import telebot
from telebot import types
from config import token
from music_parser import ParseMusic
import requests
from requests.exceptions import ConnectionError
import time

bot = telebot.TeleBot(token)


def send_films():
    CHAT_ID = '-1001336432329'
    BUY_LINK_INDEX = 0
    IMG_LINK_INDEX = 1
    CONTENT_INDEX = 2
    DOWNLOAD_LINK_INDEX = 3
    parser = ParseMusic()
    music_info = parser.parse()
    if music_info:
        music_info = dict(music_info)
        for title in music_info.keys():
            curr_music = music_info[title]
            buy_link = curr_music[BUY_LINK_INDEX]
            try:
                img = requests.get(curr_music[IMG_LINK_INDEX]).content
            except ConnectionError as conn:
                print(f'connection error {conn}')
            else:
                content = curr_music[CONTENT_INDEX]
                download_link = curr_music[DOWNLOAD_LINK_INDEX]
                bot.send_photo(CHAT_ID, photo=img, caption=f'{title}\n{content}',
                               reply_markup=keyboard(buy_link, download_link))
                time.sleep(10)



def keyboard(buy_link, download_link):
    keyboard = types.InlineKeyboardMarkup()
    download_button = types.InlineKeyboardButton(text='Download', url=download_link)
    buy_button = types.InlineKeyboardButton(text='Buy', url=buy_link)
    keyboard.row(download_button, buy_button)
    return keyboard


if __name__ == '__main__':
    send_films()
