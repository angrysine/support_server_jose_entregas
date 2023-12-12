import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
from decouple import config
from talker import Talker
from llm import ChatBotModel
import re

def get_input_position(msg):
        """
        This function purpose is to get the position from the chatbot
        using a regex, then returning it as a list of integers
        """
        input_text = msg
        match = re.findall(r'[-+]?(\d*\.\d+|\d+)([eE][-+]?\d+)?', input_text)
        print(match)
        position = [float(i[0]) for i in match]
        print(f"position: {position}")
        return position

KEY = config('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
chatbot_topic= Talker('chatbot_topic')
llm = ChatBotModel()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatbot_topic.send("run")
    print("run")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="run")


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer= llm.chat(update.message.text)
    position = get_input_position(answer)
    chatbot_topic.send(f"{position[0]},{position[1]}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text= answer)



if __name__ == '__main__':
    print(get_input_position("move to 1.0,2.0"))
    print(KEY)
    application = ApplicationBuilder().token(KEY).build()
    
    start_handler = CommandHandler('start', start)
    run_handler = CommandHandler('run', run)
    echo_handler = MessageHandler(filters.TEXT &(~filters.COMMAND), answer)


    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(run_handler)
    application.run_polling()