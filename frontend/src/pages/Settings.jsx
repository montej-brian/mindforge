/**
 * Settings — Environment and agent configuration
 */
import { useState } from 'react'
import './Settings.css'

const SETTING_GROUPS = [
  {
    title: 'AI Engine',
    icon: '🧠',
    fields: [
      { id: 'gemini-model', label: 'Gemini Model', type: 'select', options: ['gemini-1.5-pro-latest', 'gemini-1.5-flash-latest', 'gemini-1.0-pro'], defaultValue: 'gemini-1.5-pro-latest' },
    ],
  },
  {
    title: 'Voice Engine',
    icon: '🎤',
    fields: [
      { id: 'voice-engine', label: 'STT Engine', type: 'select', options: ['google', 'whisper'], defaultValue: 'google' },
      { id: 'whisper-model', label: 'Whisper Model Size', type: 'select', options: ['tiny', 'base', 'small', 'medium'], defaultValue: 'base' },
    ],
  },
  {
    title: 'Browser',
    icon: '🌐',
    fields: [
      { id: 'headless', label: 'Headless Mode', type: 'select', options: ['false', 'true'], defaultValue: 'false' },
      { id: 'timeout', label: 'Page Load Timeout (s)', type: 'number', defaultValue: '30' },
    ],
  },
]

export default function Settings() {
  const [saved, setSaved] = useState(false)

  function handleSave(e) {
    e.preventDefault()
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="fade-in">
      <div className="page-header">
        <h1 className="page-title">⚙️ Settings</h1>
        <p className="page-subtitle">Configure agents, voice engine, and browser automation</p>
      </div>

      <form className="settings-form" onSubmit={handleSave} style={{ maxWidth: 600 }}>
        {SETTING_GROUPS.map(({ title, icon, fields }) => (
          <div key={title} className="settings-group glass-card panel">
            <div className="panel-header">
              <span className="panel-title">{icon} {title}</span>
            </div>
            {fields.map(({ id, label, type, options, defaultValue }) => (
              <div key={id} className="setting-row">
                <label htmlFor={id} className="setting-label">{label}</label>
                {type === 'select' ? (
                  <select id={id} className="input" defaultValue={defaultValue} style={{ maxWidth: 240 }}>
                    {options.map((o) => <option key={o} value={o}>{o}</option>)}
                  </select>
                ) : (
                  <input id={id} type={type} className="input" defaultValue={defaultValue} style={{ maxWidth: 240 }} />
                )}
              </div>
            ))}
          </div>
        ))}

        <button id="save-settings-btn" type="submit" className="btn btn-primary" style={{ marginTop: 16 }}>
          {saved ? '✅ Saved!' : 'Save Settings'}
        </button>
      </form>

      <div className="settings-group glass-card panel" style={{ maxWidth: 600, marginTop: 'var(--space-md)' }}>
        <div className="panel-header"><span className="panel-title">🔌 API Status</span></div>
        <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>
          Backend: <span className="tag">http://localhost:8000</span> &nbsp;
          Docs: <a href="http://localhost:8000/api/docs" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-secondary)' }}>OpenAPI ↗</a>
        </p>
      </div>
    </div>
  )
}
