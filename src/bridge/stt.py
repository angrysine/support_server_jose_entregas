from decouple import config
import whisper

# from openai import OpenAI


# api_key = config("OPENAI_API_KEY")

# client = OpenAI(api_key=api_key)


class STT:
    def __init__(self, filename=None):
        self.model = whisper.load_model("medium")
        self.filename = filename


    def transcribe(self):
        if self.filename is not None:
            # load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(self.filename)
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

            # detect the spoken language
            _, probs = self.model.detect_language(mel)
            print(f"Detected language: {max(probs, key=probs.get)}")

            # decode the audio
            options = whisper.DecodingOptions(fp16=False)
            result = whisper.decode(self.model, mel, options)
            return result.text


def main():    
    # arquivo só para teste, excluir dps
    stt = STT(filename='./audio/audio.ogg')
    print(stt)
    speech_text = stt.transcribe()
    
    print(speech_text)

if __name__ == "__main__":
    main()