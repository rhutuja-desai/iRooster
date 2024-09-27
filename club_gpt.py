import time
import datetime
import picamera
import sounddevice as sd
import numpy as np
import wave
import subprocess

# Configuration
VIDEO_DURATION = 60  # seconds
AUDIO_SAMPLE_RATE = 44100  # Hz
AUDIO_CHANNELS = 2  # stereo
AUDIO_DURATION = VIDEO_DURATION  # seconds
RECORD_INTERVAL = 3600  # 1 hour in seconds

def record_audio(filename, duration):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * AUDIO_SAMPLE_RATE), samplerate=AUDIO_SAMPLE_RATE, channels=AUDIO_CHANNELS, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Audio recording complete.")

    # Save the audio data to a WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(AUDIO_CHANNELS)
        wf.setsampwidth(2)  # 16 bits = 2 bytes
        wf.setframerate(AUDIO_SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

def record_video(filename, duration):
    with picamera.PiCamera() as camera:
        camera.start_preview()
        print("Recording video...")
        camera.start_recording(filename)
        camera.wait_recording(duration)
        camera.stop_recording()
        print("Video recording complete.")

def combine_audio_video(video_file, audio_file, output_file):
    print("Combining audio and video...")
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_file
    ]
    subprocess.run(command)
    print("Combination complete.")

def main():
    while True:
        # Create timestamped filenames
        timestamp = datetime.datetime.now().strftime('%m%d_%H%M')
        video_file = f'v_{timestamp}.h264'
        audio_file = f'a_{timestamp}.wav'
        output_file = f'op_{timestamp}.mp4'

        # Record audio and video simultaneously
        record_audio(audio_file, AUDIO_DURATION)
        record_video(video_file, VIDEO_DURATION)

        # Combine audio and video
        combine_audio_video(video_file, audio_file, output_file)

        # Wait for the next recording interval
        print(f"Waiting for the next recording in {RECORD_INTERVAL} seconds...")
        time.sleep(RECORD_INTERVAL)

if __name__ == "__main__":
    main()
