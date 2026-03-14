/**
 * VoiceControl — Mic activation, waveform, and transcript display
 */
import { useState, useCallback } from 'react'
import useStore from '../store/useStore'
import { api } from '../services/api'
import './VoiceControl.css'

export default function VoiceControl() {
  const { isListening, voiceTranscript, setListening, setTranscript, addEvent } = useStore()
  const [error, setError] = useState(null)
  const [recognition, setRecognition] = useState(null)

  const startListening = useCallback(() => {
    setError(null)
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech Recognition not supported in this browser. Use Chrome.')
      return
    }
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    const rec = new SR()
    rec.lang = 'en-US'
    rec.interimResults = true
    rec.maxAlternatives = 1

    rec.onstart = () => setListening(true)
    rec.onresult = (e) => {
      const transcript = Array.from(e.results)
        .map((r) => r[0].transcript)
        .join('')
      setTranscript(transcript)
    }
    rec.onend = async () => {
      setListening(false)
      const final = useStore.getState().voiceTranscript
      if (final.trim()) {
        addEvent({ type: 'voice', message: `🎤 "${final}"` })
        try {
          await api.voice.sendCommand(final)
          await api.agents.run(final)
        } catch (err) {
          addEvent({ type: 'error', message: `Command failed: ${err.message}` })
        }
      }
    }
    rec.onerror = (e) => {
      setError(`Voice error: ${e.error}`)
      setListening(false)
    }
    rec.start()
    setRecognition(rec)
  }, [setListening, setTranscript, addEvent])

  const stopListening = useCallback(() => {
    recognition?.stop()
  }, [recognition])

  return (
    <div className="voice-control glass-card panel">
      <div className="panel-header">
        <span className="panel-title">Voice Control</span>
        <span className={`dot ${isListening ? 'dot-purple' : 'dot-gray'}`} />
      </div>

      <button
        id="voice-mic-btn"
        className={`mic-btn ${isListening ? 'mic-btn--active' : ''}`}
        onClick={isListening ? stopListening : startListening}
        aria-label={isListening ? 'Stop listening' : 'Start listening'}
      >
        {isListening ? (
          <div className="waveform">
            {Array.from({ length: 5 }).map((_, i) => (
              <span key={i} className="wave-bar" style={{ animationDelay: `${i * 0.1}s` }} />
            ))}
          </div>
        ) : (
          <span className="mic-icon">🎤</span>
        )}
      </button>

      <p className="mic-label">{isListening ? 'Listening… click to stop' : 'Click to speak a command'}</p>

      {voiceTranscript && (
        <div className="transcript-box fade-in">
          <span className="transcript-label">Heard:</span>
          <p className="transcript-text">"{voiceTranscript}"</p>
        </div>
      )}

      {error && <p className="voice-error">{error}</p>}
    </div>
  )
}
