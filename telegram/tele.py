
from telegram import Update,File
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
from decouple import config
from talker import Talker
from model import ChatBotModel
from speech_to_text import STT
from tts import TTS
import re
#topic where we will publish the points
chatbot_topic= Talker('chatbot_topic')
#Large language model 
llm = ChatBotModel()
#telegram bot token
KEY = config('TOKEN')
#flag to know if we will answer if an audio or not
audio_mode = False
def get_input_position(msg):
    """
    This function purpose is to get the position from the chatbot
    using a regex, then returning it as a list of integers
    """
    input_text = msg
    match = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', input_text)
    if not match:
        return None
    print(match)
    position = [float(i) for i in match]
    print(f"position: {position}")
    return position





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """message that will be sent when user starts chat"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ola eu sou se ajudante o Jose Entregas! Pergunte para mim em texto ou aúdio sobre a posição de qualquer item no almoxarifado, se quiser que eu responda em audio mande a mensagem: /audio_mode , se quisser que eu mande o robô buscar os items mande a mensagem: /run")


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """command that tells the robot to run"""
    chatbot_topic.send("run")
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="run")


async def audio_mode_f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """command that tells the robot to change the state of audio mode"""
    global audio_mode 
    audio_mode = not audio_mode

    await context.bot.send_message(chat_id=update.effective_chat.id, text="audio mode: "+str(audio_mode))

async def answer_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    """function that will be called when a text message is sent to the bot"""
    answer= llm.chat(update.message.text)
    position = get_input_position(answer)
    if position is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text= "não entendi o que você quis dizer, tente novamente")
        return
    chatbot_topic.send(f"{position[0]},{position[1]}")
    if audio_mode:
        tts = TTS(filename=None, text=answer)
        tts.generate_audio()
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('./audio/audio.mp3', 'rb'))
        return 
    await context.bot.send_message(chat_id=update.effective_chat.id, text= answer)

async def answer_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """function that will be called when a audio message is sent to the bot"""
    new_file = await context.bot.get_file(update.message.voice.file_id)
    with open("./audio/audio.ogg", "wb") as f:
        
        # download the voice note as a file
        await File.download_to_memory(new_file,out=f)
    stt = STT(filename='./audio/audio.ogg')
    speech_text = stt.transcribe()
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text= "entendi o seguinte do audio: "+speech_text+ " vou processar seu pedido.")
    answer =llm.chat(speech_text)
    position = get_input_position(answer)
    if position is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text= "não entendi o que você quis dizer, tente novamente")
        return
    chatbot_topic.send(f"{position[0]},{position[1]}")

    if audio_mode:
        tts = TTS(filename=None, text=answer)
        tts.generate_audio()
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('./audio/audio.mp3', 'rb'))
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text= answer)
    
  





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