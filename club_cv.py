import cv2
import numpy as np
import sounddevice as sd
import wave
import subprocess
import time
import datetime

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
    print("Recording video...")
    cap = cv2.VideoCapture(0)  # Open the default camera

    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec
    out = cv2.VideoWriter(filename, fourcc, 30.0, (640, 480))  # 640x480 resolution

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)  # Write the frame
        else:
            print("Failed to grab frame")

    cap.release()  # Release the video capture object
    out.release()  # Release the video writer
    cv2.destroyAllWindows()
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
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        video_file = f'video_{timestamp}.avi'
        audio_file = f'audio_{timestamp}.wav'
        output_file = f'output_{timestamp}.mp4'

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
