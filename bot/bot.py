import apiai
import json
import wikipedia
from googletrans import Translator


class Bot():
    def weather(self, req: str):
        print(f'Погода для запроса: {req}')

    def random_gif(self, req: str):
        return None

    def translate(self, req: str):
        return None

    def get_answer(self, req: str):
        return None

    def say_random_answer(self, req: str):
        return None

    def wiki(self, req: str):
        print(f'wiki {req}')
        try:
            wikipedia.set_lang("ru")
            return wikipedia.summary(req, sentences=4)
        except wikipedia.WikipediaException:
            return None

    dep_commands = {'погода': weather, 'wiki': wiki}
    undep_commands = [translate, get_answer, say_random_answer]

    def __init__(self):
        self.APIKEY = 'f07aa55b08e84306a74e9fef2639b1c8'

    def get_answer(self, req=''):
        for elem in self.dep_commands:
            if elem in req:
                return self.dep_commands.get(elem)(self, req.replace(elem, ''))
        for elem in self.dep_commands:
            answer = self.dep_commands.get(elem)(self, req)
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
