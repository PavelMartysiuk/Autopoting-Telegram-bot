from bs4 import BeautifulSoup
from collections import defaultdict
import json
import requests
from requests.exceptions import HTTPError


class ParseMusic:
    def __init__(self):
        self.url = 'http://www.hiphopbootleggers.net/'
        self.output_file_name = 'sent_music.json'
        self.music_info = defaultdict(list)

    def check_connect(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except HTTPError as htt_err:
            print(f'HttpError: {htt_err}')
        except Exception as exc:
            print(f'Other error: {exc}')
        else:
            return response.text

    def save_sent_music(self):
        if self.sent_music:
            self.sent_music.update(self.music_info)
            with open(self.output_file_name, 'w') as file:
                json.dump(self.sent_music, file, indent=2)
        else:
            with open(self.output_file_name, 'w') as file:
                json.dump(self.music_info, file, indent=2)

    def read_sent_music(self):
        try:
            with open(self.output_file_name) as file:
                self.sent_music = json.load(file)
        except FileNotFoundError:
            self.sent_music = None

    def parse(self):
        IMG_LINK_INDEX = 0
        CONTENT_INDEX = 1
        DOWNLOAD_INDEX = 2
        response = self.check_connect()
        if response:
            soup = BeautifulSoup(response, 'html.parser')
            music_blocks = soup.find_all('div', class_='post')
            for music_block in music_blocks:
                title = music_block.find('h2').text
                try:
                    buy_link = music_block.find('a', target='_blank').get('href')
                except AttributeError:
                    continue  # Not buy_link
                content_block = music_block.find('div', class_='entry')
                content_tags = content_block.find_all('p')
                try:
                    img_link = content_tags[IMG_LINK_INDEX].find('a').get('href')
                except AttributeError:
                    img_link = content_tags[IMG_LINK_INDEX].find('img').get('src')
                content = content_tags[CONTENT_INDEX].text
                try:
                    download_link = content_tags[DOWNLOAD_INDEX].find('a').get('href')
                except AttributeError:
                    continue
                self.read_sent_music()
                if self.sent_music:
                    sent_title = dict(self.sent_music).keys()
                    if title not in sent_title:
                        self.music_info[title].extend((buy_link, img_link, content, download_link))
                else:
                    self.music_info[title].extend((buy_link, img_link, content, download_link))
        if self.music_info:
            self.save_sent_music()
            return self.music_info
        else:
            print('Site doesnt have a new music ')


if __name__ == '__main__':
    parser = ParseMusic()
    parser.parse()
