from skpy import  SkypeEventLoop, SkypeNewMessageEvent
import apiai, json
import shelve

def help():
    print(
    """
    Чтобы воспользоваться ботом нужны следующие данные:
    Логин и пароль от скайпа
    а так же регистрация на сайте dialoglow
    """)

dialogflowtoken = None
skypemail = None 
skypepassw = None

with shelve.open('passw') as db:
    dialogflowtoken = db.get('dialogflowtoken')
    skypemail       = db.get('skypemail') 
    skypepassw      = db.get('skypepassw')
    if dialogflowtoken is None or skypemail is None or skypepassw is None:
        help()

    if not dialogflowtoken:
        db['dialogflowtoken'] = input('Введите dialogflowtoken: ').strip()
        dialogflowtoken       = db['dialogflowtoken']
    if not skypemail:
        db['skypemail']       = input('Введите email от скайп: ').strip()
        skypemail             = db['skypemail'] 
    if not skypepassw:
        db['skypepassw']      = input('Введите пароль от скайп: ').strip()
        skypepassw            = db['skypepassw']

def get_bot_respose(question = ""):
    request = apiai.ApiAI(dialogflowtoken).text_request() 
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = question
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    if responseJson:
        return responseJson['result']['fulfillment']['speech']
    else:
        return "Извините, я не понял вопроса, я пока что только учусь"

class Skype(SkypeEventLoop):
    def onEvent(self, event):
        if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId:
            ansnwer = get_bot_respose(event.msg.content)
            event.msg.chat.sendMsg(ansnwer)

skype = Skype(skypemail, skypepassw,'token.txt')
while True:
    try:
        print('SkypeBot работает')
        skype.loop()
    except Exception as e:
        print(e)
        skype = Skype(skypemail, skypepassw, 'token.txt')
