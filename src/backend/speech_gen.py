from gtts import gTTS
from gtts.tokenizer import Tokenizer, pre_processors, tokenizer_cases

from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import time
import os

img_data_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/gen_data/"

class GoogleTextToSpeech():
    def __init__(self):
        self.bytes_obj = BytesIO()

    def generate_speech(self, spec_text):
        self.bytes_obj = BytesIO()

        gtts = gTTS(text=spec_text, lang="cs")
        gtts.write_to_fp(self.bytes_obj)
        gtts.save(os.path.join(img_data_path, 'audio.mp3'))

        #self.play_audio()

    def play_audio(self):
        self.bytes_obj.seek(0)
        song = AudioSegment.from_file(self.bytes_obj, sample_width=2, frame_rate=44100, channels=1)
        play(song)