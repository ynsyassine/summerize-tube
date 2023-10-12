import pytube
from IPython.display import Audio, display
from pydub import AudioSegment
from transformers import pipeline
import tempfile
from pytube import YouTube
from IPython.display import Audio
import tempfile
import os





#define the  function that retreive the audio from a url video
def get_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_filename = "audio.mp3"
    audio_stream.download(filename=audio_filename)
    # Play the audio
    display(Audio(filename=audio_filename, autoplay=True))
    return audio_filename


# def get_audio(url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': 'temp_audio.mp3',  # name the file
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#     return 'temp_audio.mp3'


# Split audio into 30-second chunks
def return_chunks(name):
    audio = AudioSegment.from_file(name)
    chunks = [chunk for chunk in audio[::30 * 1000]]
    return chunks

#  Transcribe each chunk
def transcript_chunk(chunks):
    whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium', device=0)
    transcriptions = []
    for index, chunk in enumerate(chunks):
        chunk_filename = f"chunk{index}.mp3"
        chunk.export(chunk_filename, format="mp3")
        transcription = whisper(chunk_filename)  # Pass the file path instead of raw data
        transcriptions.append(transcription)
    # Step 3: Combine the transcriptions
    full_script = ' '.join(t["text"] for t in transcriptions)
    return full_script




#printing for full script
def display_full_script(full_script):
    return full_script




def chunk_text(text, max_length):
    chunks = []
    words = text.split()
    current_chunk = ""
    for word in words:
        if len(current_chunk + word) < max_length:
            current_chunk += " " + word
        else:
            chunks.append(current_chunk)
            current_chunk = word
    chunks.append(current_chunk)
    return chunks

def final_sammurize(text):

    # Create a summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Split the text into chunks
    max_length = 1024  # Max token limit for the model

    chunks = chunk_text(text, max_length)
    # Summarize each chunk
    summaries = [summarizer(chunk, max_length=100, min_length=25, do_sample=False)[0]['summary_text'] for chunk in chunks]

    # Combine the summaries
    final_summary = " ".join(summaries)

    # Output the final summary
    return final_summary