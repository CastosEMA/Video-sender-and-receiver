import asyncio
import socket
import json
import base64
import cv2
import numpy as np

async def receive_video():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 25544))
    server_socket.listen(1)
    print("Server started. Waiting for connection...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client {addr} connected")

        data = b""
        while True:
            chunk = client_socket.recv(10240)
            if not chunk:
                break
            data += chunk

        if data:
            frame_base64 = data.decode('utf-8')
            frame_bytes = base64.b64decode(frame_base64)

            yield frame_bytes

async def display_video():
    async for frame_bytes in receive_video():
        try:
            frame = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = frame.reshape(480, 640, 3)  # Adjust dimensions as needed

            # Display the frame using OpenCV
            cv2.imshow('Decoded Video', frame)
            cv2.waitKey(1)
        except Exception as e:
            print(f"Error displaying video: {e}")

        await asyncio.sleep(0)

async def main():
    await display_video()

if __name__ == "__main__":
    asyncio.run(main())
