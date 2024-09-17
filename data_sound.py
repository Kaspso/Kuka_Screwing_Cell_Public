import pyaudio
import threading
import wave
class SoundRecorderThread(threading.Thread):
    def __init__(self):
        # Call the constructor of the parent class (threading.Thread)
        threading.Thread.__init__(self)
        
        # Initialize some default parameters for recording audio
        self.frames = []
        self.should_stop = False
        self.CHUNK = 1024 #buffer
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

    def run(self):
        audio = pyaudio.PyAudio()
        # Open a stream for recording audio with the default input device
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        # Continuously read audio data from the stream and append it to self.frames
        while not self.should_stop:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            
        # Stop the stream and close it
        stream.stop_stream()
        stream.close()
        audio.terminate()

    # Set the should_stop flag to True, which will cause the recording loop to exit
    def stop_recording(self):
        self.should_stop = True

    # Return the list of recorded audio frames
    def get_frames(self):
        return self.frames

# Function that saves recordings
def save_recording(frames, filename):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
