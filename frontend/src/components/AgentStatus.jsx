/**
 * AgentStatus — Real-time display of all agent states
 */
import useStore from '../store/useStore'
import './AgentStatus.css'

const AGENT_CONFIGS = [
  { key: 'orchestrator', label: 'Orchestrator',  icon: '🧠' },
  { key: 'browser',      label: 'Browser Agent', icon: '🌐' },
  { key: 'voice',        label: 'Voice Agent',   icon: '🎤' },
  { key: 'assignment',   label: 'AI Solver',     icon: '✏️' },
]

function statusDot(status) {
  switch (status) {
    case 'running': return 'dot-purple'
    case 'idle':    return 'dot-green'
    case 'error':   return 'dot-red'
    default:        return 'dot-gray'
  }
}

function statusBadge(status) {
  switch (status) {
    case 'running': return 'badge-running'
    case 'idle':    return 'badge-done'
    case 'error':   return 'badge-failed'
    default:        return 'badge-pending'
  }
}

export default function AgentStatus() {
  const agents = useStore((s) => s.agents)
  const wsConnected = useStore((s) => s.wsConnected)

  return (
    <div className="agent-status glass-card panel">
      <div className="panel-header">
        <span className="panel-title">Agent Status</span>
        <div className="ws-indicator">
          <span className={`dot ${wsConnected ? 'dot-green' : 'dot-red'}`} />
          <span className="ws-label">{wsConnected ? 'Live' : 'Disconnected'}</span>
        </div>
      </div>

      <div className="agent-list">
        {AGENT_CONFIGS.map(({ key, label, icon }) => {
          const { status, message } = agents[key]
          return (
            <div key={key} className="agent-row" id={`agent-${key}`}>
              <span className="agent-icon">{icon}</span>
              <div className="agent-info">
                <span className="agent-name">{label}</span>
                {message && <span className="agent-msg">{message}</span>}
              </div>
              <div className="agent-status-right">
                <span className={`dot ${statusDot(status)}`} />
                <span className={`badge ${statusBadge(status)}`}>{status}</span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
