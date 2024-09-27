import speech_recognition as sr
import sounddevice as sd
import wave
import time

def record_audio(filename, duration=5):
    fs = 44100  
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait() 
    print("Recording finished.")
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Ready to listen for 'Edubot'.")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)

                if "Edubot" in command:
                    record_audio("recording.wav", duration=5)
                    print("Audio recorded for 5 seconds.")
             
            except sr.UnknownValueError:
                continue 
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()
