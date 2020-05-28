import apiai
import json


class Bot():
    def weather(self, req: str):
        print(f'Погода для запроса: {req}')

    def random_gif(self, req: str):
        return " gif "

    def translate(self, req: str):
        return 'tranlate'

    def get_answer(self, req: str):
        return 'getanswer'

    def say_random_answer(self, req: str):
        return 'sayrandomanswer'

    dep_commands = {'погода': weather, }
    undep_commands = [translate, get_answer, say_random_answer]

    def __init__(self):
        self.APIKEY = 'f07aa55b08e84306a74e9fef2639b1c8'

    def get_answer(self, req=''):
        for elem in self.dep_commands:
            if elem in req:
                return self.dep_commands.get(elem)(self, req=req)
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
