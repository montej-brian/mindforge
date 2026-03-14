/**
 * MINDFORGE — WebSocket Client
 * Connects to ws://localhost:8000/ws/events and dispatches events to global store.
 */
import useStore from '../store/useStore'

const WS_URL = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws/events`

let socket = null
let reconnectTimer = null
const RECONNECT_DELAY = 3000

function dispatch(event) {
  const store = useStore.getState()
  const { type, data } = event

  switch (type || event.event) {
    case 'agent_started':
      store.updateAgent(data?.agent || 'orchestrator', { status: 'running', message: data?.message || '' })
      break
    case 'agent_step':
      store.addEvent({ type: 'step', agent: data?.agent, message: data?.message })
      break
    case 'agent_completed':
      store.updateAgent(data?.agent || 'orchestrator', { status: 'idle', message: 'Completed' })
      store.addEvent({ type: 'success', message: data?.output || 'Task complete' })
      break
    case 'agent_error':
      store.updateAgent(data?.agent || 'orchestrator', { status: 'error', message: data?.error || 'Unknown error' })
      store.addEvent({ type: 'error', message: data?.error })
      break
    case 'browser_action':
      store.setCurrentUrl(data?.url || '')
      store.addEvent({ type: 'browser', message: data?.action })
      break
    case 'voice_detected':
      store.setTranscript(data?.transcript || '')
      break
    case 'status_update':
      store.addEvent({ type: 'info', message: data?.message })
      break
    default:
      break
  }
}

export function connectWebSocket() {
  if (socket?.readyState === WebSocket.OPEN) return

  socket = new WebSocket(WS_URL)

  socket.onopen = () => {
    useStore.getState().setWsConnected(true)
    useStore.getState().addEvent({ type: 'info', message: '🔗 WebSocket connected' })
    clearTimeout(reconnectTimer)
  }

  socket.onmessage = (e) => {
    try {
      const event = JSON.parse(e.data)
      dispatch(event)
    } catch {
      console.warn('WS parse error:', e.data)
    }
  }

  socket.onclose = () => {
    useStore.getState().setWsConnected(false)
    reconnectTimer = setTimeout(connectWebSocket, RECONNECT_DELAY)
  }

  socket.onerror = (err) => {
    console.error('WebSocket error:', err)
  }
}

export function sendWsMessage(payload) {
  if (socket?.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(payload))
  }
}

export function disconnectWebSocket() {
  clearTimeout(reconnectTimer)
  socket?.close()
}
