/**
 * Dashboard — Main control panel
 */
import { useEffect } from 'react'
import VoiceControl from '../components/VoiceControl'
import AgentStatus from '../components/AgentStatus'
import TaskQueue from '../components/TaskQueue'
import BrowserPreview from '../components/BrowserPreview'
import { connectWebSocket } from '../services/websocket'
import useStore from '../store/useStore'
import './Dashboard.css'

function EventLog() {
  const events = useStore((s) => s.events)
  const clearEvents = useStore((s) => s.clearEvents)
  return (
    <div className="event-log glass-card panel">
      <div className="panel-header">
        <span className="panel-title">Event Log</span>
        <button className="btn btn-ghost" style={{ padding: '4px 10px', fontSize: 11 }} onClick={clearEvents}>Clear</button>
      </div>
      <div className="event-list" id="event-log-list">
        {events.length === 0 && <p className="empty-state">No events yet.</p>}
        {events.map((ev) => (
          <div key={ev.id} className={`event-item event-${ev.type} fade-in`}>
            <span className="event-time">{new Date(ev.timestamp).toLocaleTimeString()}</span>
            <span className="event-msg">{ev.message}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

function StatCard({ icon, label, value, color }) {
  return (
    <div className="stat-card glass-card">
      <div className="stat-icon" style={{ color }}>{icon}</div>
      <div className="stat-body">
        <span className="stat-value">{value}</span>
        <span className="stat-label">{label}</span>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const tasks = useStore((s) => s.tasks)
  const wsConnected = useStore((s) => s.wsConnected)

  useEffect(() => { connectWebSocket() }, [])

  const pending   = tasks.filter((t) => t.status === 'pending').length
  const running   = tasks.filter((t) => t.status === 'running').length
  const completed = tasks.filter((t) => t.status === 'completed').length

  return (
    <div className="dashboard fade-in">
      <div className="page-header">
        <h1 className="page-title">🧠 MINDFORGE Dashboard</h1>
        <p className="page-subtitle">Voice-controlled multi-agent assignment automation</p>
      </div>

      <div className="stats-row">
        <StatCard icon="📋" label="Pending"   value={pending}   color="var(--accent-yellow)" />
        <StatCard icon="⚡" label="Running"   value={running}   color="var(--accent-secondary)" />
        <StatCard icon="✅" label="Completed" value={completed} color="var(--accent-green)" />
        <StatCard icon="🔗" label="WS Status" value={wsConnected ? 'Live' : 'Off'} color={wsConnected ? 'var(--accent-green)' : 'var(--accent-red)'} />
      </div>

      <div className="dashboard-grid">
        <div className="col-left">
          <VoiceControl />
          <AgentStatus />
        </div>
        <div className="col-center">
          <BrowserPreview />
          <EventLog />
        </div>
        <div className="col-right">
          <TaskQueue />
        </div>
      </div>
    </div>
  )
}
