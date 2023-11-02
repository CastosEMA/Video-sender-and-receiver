# Video Streaming Application

This application consists of two Python scripts that interact with each other to stream video and audio data over a network. The first script captures video and audio data from the user's device and sends it to a server. The second script receives this data from the server and displays it.

## Script 1: Video and Audio Capture

The first script (`sender.py`) opens the default camera and microphone on the user's device using OpenCV and PyAudio, respectively. It captures video frames and audio chunks in real-time.

The captured video frames are converted to bytes, and the audio data is already in byte format. Both are then sent to a server via a socket connection.

The server's IP address and port number are hardcoded into the script ('localhost', 25544). If the server is not listening on the specified port, an error message is printed, but the program continues to run.

## Script 2: Video Display

The second script (`receiver.py`) listens for incoming connections on the same port number. When it accepts a connection, it receives the video frame bytes from the client.

The received bytes are decoded back into an image using NumPy and reshaped to their original dimensions. The image is then displayed using OpenCV.

## Running the Application

To run this application, you need to start both scripts. Start `receiver.py` first so that it can begin listening for incoming connections. Then start `sender.py` to begin capturing video and audio data and sending it to the server.

Please ensure that both scripts are running on machines that have access to each other over the network.

## Dependencies

This application requires Python 3.7 or later, as well as the following Python libraries:

- asyncio
- socket
- json
- base64
- cv2 (OpenCV)
- numpy
- pyaudio
