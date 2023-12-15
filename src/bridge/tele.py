import logging
from telegram import Update,File
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
from decouple import config
from talker import Talker
from llm import ChatBotModel
from stt import STT
from tts import TTS
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

audio_mode = False
async def audio_mode_f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global audio_mode 
    audio_mode = not audio_mode

    await context.bot.send_message(chat_id=update.effective_chat.id, text="audio mode: "+str(audio_mode))

async def answer_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer= llm.chat(update.message.text)
    position = get_input_position(answer)
    chatbot_topic.send(f"{position[0]},{position[1]}")
    if audio_mode:
        tts = TTS(filename=None, text=answer)
        tts.generate_audio()
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('./audio/audio.mp3', 'rb'))
        return 
    await context.bot.send_message(chat_id=update.effective_chat.id, text= answer)

async def answer_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_file = await context.bot.get_file(update.message.voice.file_id)
    with open("./audio/audio.ogg", "wb") as f:
        
        # download the voice note as a file
        await File.download_to_memory(new_file,out=f)
    stt = STT(filename='./audio/audio.ogg')
    speech_text = stt.transcribe()
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text= "entendi o seguinte do audio: "+speech_text+ " vou processar seu pedido.")
    answer =llm.chat(speech_text)
    position = get_input_position(answer)
    chatbot_topic.send(f"{position[0]},{position[1]}")
    if audio_mode:
        tts = TTS(filename=None, text=answer)
        tts.generate_audio()
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('./audio/audio.mp3', 'rb'))
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text= answer)
    
    print("recebi um audio")

    # await context.bot.send_message(chat_id=update.effective_chat.id, text= "recebi um audio")



if __name__ == '__main__':
    
    application = ApplicationBuilder().token(KEY).build()
    
    start_handler = CommandHandler('start', start)
    run_handler = CommandHandler('run', run)
    message_handler = MessageHandler(filters.TEXT &(~filters.COMMAND), answer_text)
    audio_handler = MessageHandler(filters.VOICE, answer_audio)
    audio_mode_handler = CommandHandler('audio_mode', audio_mode_f)

    application.add_handler(start_handler)
    application.add_handler(message_handler)
    application.add_handler(run_handler)
    application.add_handler(audio_handler)
    application.add_handler(audio_mode_handler)
    application.run_polling()