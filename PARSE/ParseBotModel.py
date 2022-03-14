import telegram
from telegram.ext import Updater, CommandHandler

class ParseBot:
    def __init__(self, name, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)
        self.id = 628281989
        self.name = name

    def sendMessage(self, text):
        self.core.sendMessage(chat_id = self.id, text=text)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()
        
class Hnanii(ParseBot):
    def __init__(self):
        self.token = '5005592604:AAGX4MPE0G16VwSLdpmRVvXG_rafU_uKgzA'
        ParseBot.__init__(self, '흐난', self.token)
        self.updater.stop()

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def start(self):
        self.sendMessage('Hnan system 가동.')
        self.updater.start_polling()
        self.updater.idle()