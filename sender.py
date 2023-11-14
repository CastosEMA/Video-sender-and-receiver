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


def get_my_ip_address():
    # Створити сокет для отримання IP-адреси
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # З'єднання з публічним DNS-сервером, наприклад, Google Public DNS
        my_socket.connect(('8.8.8.8', 80))
        # Отримати IP-адресу, до якої підключено сокет
        my_ip_address = my_socket.getsockname()[0]
    except Exception as e:
        my_ip_address = None
    finally:
        my_socket.close()

    return my_ip_address

import base64

SEND_VIDEO = True

nest_asyncio.apply()

# Audio recording settings
audio_stream = pa.PyAudio()
audio_format = pa.paInt16  # Audio data format
audio_channels = 1  # Number of audio channels (1 for mono, 2 for stereo)
audio_rate = 44100  # Sampling rate (hertz)
audio_chunk = 1024  # Data block size

audio_recorder = audio_stream.open(
    format=audio_format,
    channels=audio_channels,
    rate=audio_rate,
    input=True,
    frames_per_buffer=audio_chunk
)

async def send_message(send_to="", message="", info=""):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(send_to)
        ndata = {"message": message,
                "sender_ip":get_my_ip_address(),
                "info": info}
        data = json.dumps(ndata)
        client_socket.send(data.encode('utf-8'))
        client_socket.close()
    except Exception as e:
        print(f"An error of type {type(e)} occurred: {e}")

async def send_frame(frame):
    frame_base64 = base64.b64encode(frame).decode('utf-8')
    try:
        await send_message(('localhost', 25544), frame_base64, "video frame")
    except Exception as e:
        print(f"An error of type {type(e)} occurred: {e}")

async def record_video():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if ret and SEND_VIDEO:
            audio_data = audio_recorder.read(audio_chunk, exception_on_overflow=False)
            frame_bytes = frame.tobytes()
            audio_bytes = audio_data

            await send_frame(frame_bytes)

            await asyncio.sleep(0)


async def main():
    await record_video()

if __name__ == "__main__":
    asyncio.run(main())
