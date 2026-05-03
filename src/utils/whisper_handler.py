"""Whisper integration for speech transcription."""

import io
import wave
import whisper
import sounddevice as sd
import numpy as np
from pathlib import Path


class WhisperTranscriber:
    """Handle speech recording and transcription using Whisper."""
    
    def __init__(self, model_size: str = 'base', device: str = 'cuda'):
        """
        Initialize Whisper transcriber.
        
        Args:
            model_size: 'tiny', 'base', 'small', 'medium', 'large'
            device: 'cuda' or 'cpu'
        """
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size, device=device)
        self.sample_rate = 16000
        print("Whisper model loaded successfully")
    
    def record_speech(self, duration: int = 8, sample_rate: int = 16000) -> np.ndarray:
        """
        Record audio from microphone.
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Sample rate (default 16kHz for Whisper)
        
        Returns:
            NumPy array of audio samples
        """
        print(f"Recording for {duration} seconds... (speak now)")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, 
                       channels=1, dtype='float32')
        sd.wait()
        print("Recording complete")
        return audio.flatten()
    
    def save_audio(self, audio: np.ndarray, filepath: str, 
                   sample_rate: int = 16000):
        """Save audio array to WAV file."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert float32 to int16
        audio_int16 = (audio * 32767).astype(np.int16)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())
    
    def transcribe(self, audio_source, language: str = 'da') -> str:
        """
        Transcribe audio to text.
        
        Args:
            audio_source: Either a NumPy array or path to audio file
            language: Language code (e.g., 'da' for Danish)
        
        Returns:
            Transcribed text
        """
        if isinstance(audio_source, str):
            # Load from file
            print(f"Transcribing {audio_source}...")
            result = self.model.transcribe(audio_source, language=language)
        else:
            # Transcribe from NumPy array
            print("Transcribing audio...")
            result = self.model.transcribe(audio_source, language=language)
        
        text = result.get('text', '').strip()
        return text
    
    def record_and_transcribe(self, duration: int = 8, language: str = 'da') -> str:
        """
        Record speech and immediately transcribe it.
        
        Args:
            duration: Recording duration in seconds
            language: Language code
        
        Returns:
            Transcribed text
        """
        audio = self.record_speech(duration, self.sample_rate)
        text = self.transcribe(audio, language)
        return text


# Singleton instance (lazy loaded)
_transcriber = None

def get_transcriber(model_size: str = 'base', device: str = 'cpu') -> WhisperTranscriber:
    """Get or create a Whisper transcriber instance."""
    global _transcriber
    if _transcriber is None:
        _transcriber = WhisperTranscriber(model_size=model_size, device=device)
    return _transcriber


if __name__ == '__main__':
    print("=" * 70)
    print("WHISPER TRANSCRIBER TEST")
    print("=" * 70)
    
    transcriber = get_transcriber(model_size='base', device='cpu')
    
    print("\nTest: Record 5 seconds and transcribe")
    print("Instructions: Speak a simple Danish phrase")
    
    try:
        text = transcriber.record_and_transcribe(duration=5, language='da')
        print(f"\nTranscribed: {text}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This requires a working microphone and speaker")
