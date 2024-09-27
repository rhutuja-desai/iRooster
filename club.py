from picamera2.encoders import H264Encoder
from picamera2 import Picamera2
import time
import pyaudio
import wave
import datetime
from threading import Thread
import os

def record_audio(filename, duration):
    RESPEAKER_RATE = 16000
    RESPEAKER_CHANNELS = 1
    RESPEAKER_WIDTH = 2
    # run getDeviceInfo.py to get index
    RESPEAKER_INDEX = 2 # refer to input device id
    # CHUNK = 1024
    CHUNK = 2048
    RECORD_SECONDS = duration
    WAVE_OUTPUT_FILENAME = "output0.wav"

    p = pyaudio.PyAudio()

    stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                input=True,
                input_device_index=RESPEAKER_INDEX,)

    print("* recording")

    frames = []

    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        # data = stream.read(CHUNK)
        try:
            data = stream.read(CHUNK)
        except IOError as e:
            print(f"Error recording audio: {e}")
            break
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(RESPEAKER_CHANNELS)
    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
    wf.setframerate(RESPEAKER_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def record_video(filename, duration):
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    encoder = H264Encoder(bitrate=10000000)
    output = "output0.h264"
    picam2.start_recording(encoder, output)
    time.sleep(duration)
    picam2.stop_recording()

def main():
    duration = 5  # seconds
    timestamp = datetime.now().strftime("%Y:%m:%d_%H:%M:%S")

    audio_filename = f"audio_{timestamp}.wav"
    video_filename = f"video_{timestamp}.h264"

    # Start recording audio and video simultaneously
    audio_thread = Thread(target=record_audio, args=(audio_filename, duration))
    video_thread = Thread(target=record_video, args=(video_filename, duration))

    audio_thread.start()
    video_thread.start()

    audio_thread.join()
    video_thread.join()

    # Convert video to mp4
    mp4_filename = f"video_{timestamp}.mp4"
    command = f"ffmpeg -framerate 30 -i {video_filename} -c:v libx264 -preset slow -crf 22 {mp4_filename}"
    
    # Check if ffmpeg command executed successfully
    result = os.system(command)
    if result != 0:
        print("Error converting video to mp4")

    print(f"Audio and video recording saved as {audio_filename} and {mp4_filename}")