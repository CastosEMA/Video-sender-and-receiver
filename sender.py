import asyncio
import json
import socket
import time
import numpy as np
import cv2
import nest_asyncio
import pyaudio as pa
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription, RTCIceGatherer
from aiortc.contrib.signaling import BYE, object_from_string, object_to_string
from loguru import logger
import base64

SEND_VIDEO = True

nest_asyncio.apply()

# Налаштування аудіозапису
audio_stream = pa.PyAudio()
audio_format = pa.paInt16  # Формат аудіоданих
audio_channels = 1  # Кількість аудіоканалів (1 для моно, 2 для стерео)
audio_rate = 44100  # Частота дискретизації (герц)
audio_chunk = 1024  # Розмір блоку даних

audio_recorder = audio_stream.open(
    format=audio_format,
    channels=audio_channels,
    rate=audio_rate,
    input=True,
    frames_per_buffer=audio_chunk
)

def send_frame(frame):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 25544))
        frame_base64 = base64.b64encode(frame).decode('utf-8')
        client_socket.send(frame_base64.encode('utf-8'))
    except ConnectionRefusedError:
        print("Порт не слухає, але програма продовжує працювати")
    finally:
        client_socket.close()

async def record_video():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if ret and SEND_VIDEO:
            audio_data = audio_recorder.read(audio_chunk, exception_on_overflow=False)
            frame_bytes = frame.tobytes()
            audio_bytes = audio_data

            send_frame(frame_bytes)

            await asyncio.sleep(0)

async def main():
    await record_video()

if __name__ == "__main__":
    asyncio.run(main())
