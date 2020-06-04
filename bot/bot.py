import json
from random import choice

import apiai
import giphy_client
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
        self.dialogflow_key = None
        self.giphy_key = None

    def set_keys(self, dialogflow_key: str, giphy_key: str):
        self.dialogflow_key = dialogflow_key
        self.giphy_key = giphy_key

    def get_fortune(self, req: str):
        for zodiac in self.zodiac_dict:
            if zodiac in req:
                r = requests.get('https://1001goroskop.ru/', params={'znak': self.zodiac_dict.get(zodiac)})
                soup = BeautifulSoup(r.text, 'html.parser')
                return soup.find(itemprop='description').get_text()

    def weather(self, req: str):
        # img = Image.open(BytesIO(requests.get(f"http://wttr.in/{req.strip()}.png").content))
        # img.show()
        return requests.get(f"http://wttr.in/{req.strip()}.png").url

    def random_gif(self, req: str):
        api_instance = giphy_client.DefaultApi()
        #api_key = 'XPY9nG1Z28Ypu2mK8wrHGEzC8UAZW1Ts'
        api_response = api_instance.gifs_search_get(self.giphy_key, req.strip(), lang='ru')
        data = api_response.data
        result = choice(data)
        return result.images.original.url

    def translate(self, req: str):
        translator = Translator()
        inp_lang = translator.detect(req).lang
        if inp_lang != 'ru':
            translations = translator.translate([req], dest='ru')
            for translation in translations:
                if translator.detect(translation.text).lang != inp_lang:
                    return translation.text

    def get_answer(self, req: str):
        request = apiai.ApiAI(self.dialogflow_key).text_request()
        request.lang = 'ru'
        request.session_id = 'BatlabAIBot'
        request.query = req
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']
        return response

    def wiki(self, req: str):
        try:
            wikipedia.set_lang("ru")
            return wikipedia.summary(req, sentences=4)
        except wikipedia.WikipediaException:
            return None

    dep_commands = {'погода': weather, 'wiki': wiki, '-w': weather, '-gif': random_gif}
    undep_commands = [translate, get_fortune, get_answer]

    def get_answer(self, req: str):
        for elem in self.dep_commands:
            if elem in req:
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
