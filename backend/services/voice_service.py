"""
MINDFORGE — Voice Service
Speech-to-text (STT) and text-to-speech (TTS) wrapper.
Supports: Google STT (default) or OpenAI Whisper (configurable via VOICE_ENGINE).
"""
import io
import logging
import threading
from typing import Optional

import speech_recognition as sr
from gtts import gTTS

from config import settings

logger = logging.getLogger(__name__)


class VoiceService:
    """Handles microphone input (STT) and audio playback (TTS)."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = settings.voice_engine
        self._speaking = False

    # ─── Speech to Text ───────────────────────────────────────────────────────

    def listen(self, timeout: int = 10, phrase_limit: int = 30) -> Optional[str]:
        """
        Listen for a voice command from the default microphone.
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_limit: Max seconds to listen after speech starts
            
        Returns:
            Transcribed string, or None on failure
        """
        try:
            with sr.Microphone(sample_rate=settings.audio_sample_rate) as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                logger.info(f"🎤 Listening (timeout={timeout}s)...")
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )

            if self.engine == "whisper":
                return self._transcribe_whisper(audio)
            else:
                return self._transcribe_google(audio)

        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except Exception as e:
            logger.error(f"Voice listen error: {e}")
            return None

    def transcribe_audio_bytes(self, audio_bytes: bytes) -> Optional[str]:
        """
        Transcribe raw audio bytes (e.g. from an uploaded .wav file).
        Used by the /api/voice/command REST endpoint.
        """
        try:
            audio = sr.AudioData(audio_bytes, settings.audio_sample_rate, 2)
            return self._transcribe_google(audio)
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return None

    def _transcribe_google(self, audio: sr.AudioData) -> Optional[str]:
        try:
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Google STT: '{text}'")
            return text
        except sr.RequestError as e:
            logger.error(f"Google STT API error: {e}")
            return None

    def _transcribe_whisper(self, audio: sr.AudioData) -> Optional[str]:
        try:
            text = self.recognizer.recognize_whisper(
                audio, model=settings.whisper_model_size
            )
            logger.info(f"Whisper STT: '{text}'")
            return text
        except Exception as e:
            logger.error(f"Whisper STT error: {e}")
            return None

    # ─── Text to Speech ───────────────────────────────────────────────────────

    def speak(self, text: str, lang: str = "en") -> None:
        """Convert text to speech and play it in a background thread."""
        def _play():
            self._speaking = True
            try:
                tts = gTTS(text=text, lang=lang, slow=False)
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                buf.seek(0)
                # Play using mpg123 or similar available player
                import tempfile, os, subprocess
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                    f.write(buf.read())
                    tmpfile = f.name
                subprocess.run(["mpg123", "-q", tmpfile], check=False)
                os.unlink(tmpfile)
            except Exception as e:
                logger.error(f"TTS error: {e}")
            finally:
                self._speaking = False

        t = threading.Thread(target=_play, daemon=True)
        t.start()

    @property
    def is_speaking(self) -> bool:
        return self._speaking
