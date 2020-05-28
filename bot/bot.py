import json

import apiai
import requests
import wikipedia
from bs4 import BeautifulSoup
from googletrans import Translator


class Bot():
    zodiac_dict = {'овен': 'aries',
                   'телец': 'taurus',
                   'близнецы': 'gemini',
                   'рак': 'cancer',
                   'лев': 'leo',
                   'дева': 'virgo',
                   'весы': 'libra',
                   'скорпион': 'scorpio',
                   'стрелец': 'sagittarius',
                   'козерог': 'capricorn',
                   'водолей': 'aquarius',
                   'рыбы': 'pisces',
                   }

    def __init__(self):
        self.APIKEY = 'f07aa55b08e84306a74e9fef2639b1c8'

    def get_fortune(self, req: str):
        for zodiac in self.zodiac_dict:
            if zodiac in req:
                r = requests.get('https://1001goroskop.ru/', params={'znak': self.zodiac_dict.get(zodiac)})
                soup = BeautifulSoup(r.text, 'html.parser')
                return soup.find(itemprop='description').get_text()

    def weather(self, req: str):
        return None

    def random_gif(self, req: str):
        return None

    def translate(self, req: str):
        translator = Translator()
        inp_lang = translator.detect(req).lang
        if inp_lang != 'ru':
            translations = translator.translate([req], dest='ru')
            for translation in translations:
                if translator.detect(translation.text).lang != inp_lang:
                    return translation.text

    def get_answer(self, req: str):
        request = apiai.ApiAI(self.APIKEY).text_request()
        request.lang = 'ru'
        request.session_id = 'BatlabAIBot'
        request.query = req
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']
        return response

    def wiki(self, req: str):
        print(f'wiki {req}')
        try:
            wikipedia.set_lang("ru")
            return wikipedia.summary(req, sentences=4)
        except wikipedia.WikipediaException:
            return None

    dep_commands = {'погода': weather, 'wiki': wiki}
    undep_commands = [translate, get_fortune, get_answer]

    def get_answer(self, req: str):
        for elem in self.dep_commands:
            if elem in req:
                print(elem + ' is in ' + req)
                return self.dep_commands.get(elem)(self, req.replace(elem, ''))

        for elem in self.undep_commands:
            answer = elem(self, req)
            if answer is not None:
                return answer
        return " -- "


if __name__ == "__main__":
    bot = Bot()
    while True:
        req = input("Задайте вопрос боту: ")
        if 'exit' in req:
            break
        answer = bot.get_answer(req)
        print(answer)
