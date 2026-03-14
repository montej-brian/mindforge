"""
MINDFORGE — Voice API Routes
POST /api/voice/command — accepts transcript text or audio bytes, returns parsed intent + task ID.
POST /api/voice/speak   — TTS: returns spoken text confirmation.
"""
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional

from models.schemas import VoiceCommandRequest, VoiceCommandResponse
from agents.voice_agent import VoiceAgent

router = APIRouter()
logger = logging.getLogger(__name__)
_voice_agent = VoiceAgent()


@router.post("/command", response_model=VoiceCommandResponse)
async def process_voice_command(request: VoiceCommandRequest):
    """
    Process a voice command.
    Accepts either a transcript string (pre-transcribed) or audio_url reference.
    Returns the parsed intent and a spawned task ID.
    """
    transcript = request.transcript
    if not transcript:
        raise HTTPException(status_code=400, detail="transcript is required")

    logger.info(f"Voice command received: {transcript}")
    intent = await _voice_agent.process_command(transcript)

    return VoiceCommandResponse(transcript=transcript, intent=intent)


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """
    Accept raw audio file upload (.wav) for server-side transcription.
    Returns transcript and parsed intent.
    """
    if not file.filename.endswith((".wav", ".mp3", ".ogg")):
        raise HTTPException(status_code=400, detail="Only .wav, .mp3, .ogg files accepted")

    audio_bytes = await file.read()
    from services.voice_service import VoiceService
    vs = VoiceService()
    transcript = vs.transcribe_audio_bytes(audio_bytes)

    if not transcript:
        raise HTTPException(status_code=422, detail="Could not transcribe audio")

    intent = await _voice_agent.process_command(transcript)
    return {"transcript": transcript, "intent": intent}


@router.post("/speak")
async def speak(text: str = Form(...)):
    """Convert text to speech (fire and forget — plays on server)."""
    _voice_agent.speak(text)
    return {"message": f"Speaking: {text[:50]}..."}
