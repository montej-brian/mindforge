/**
 * MINDFORGE — REST API Client
 * All backend requests proxied via Vite → http://localhost:8000
 */

const BASE = '/api'

async function request(method, path, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (body) opts.body = JSON.stringify(body)

  const res = await fetch(`${BASE}${path}`, opts)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.status === 204 ? null : res.json()
}

// ─── Health ────────────────────────────────────────────────────────────────
export const api = {
  health: () => request('GET', '/health'),

  // ─── Voice ──────────────────────────────────────────────────────────────
  voice: {
    sendCommand: (transcript) =>
      request('POST', '/voice/command', { transcript }),
    speak: (text) => {
      const form = new FormData()
      form.append('text', text)
      return fetch(`${BASE}/voice/speak`, { method: 'POST', body: form }).then((r) => r.json())
    },
  },

  // ─── Agents ─────────────────────────────────────────────────────────────
  agents: {
    run: (command, context) => request('POST', '/agents/run', { command, context }),
    status: (taskId) => request('GET', `/agents/status/${taskId}`),
    list: () => request('GET', '/agents/tasks'),
    cancel: (taskId) => request('DELETE', `/agents/tasks/${taskId}`),
  },

  // ─── Tasks ──────────────────────────────────────────────────────────────
  tasks: {
    create: (payload) => request('POST', '/tasks/', payload),
    list: (params = {}) => {
      const qs = new URLSearchParams(params).toString()
      return request('GET', `/tasks/${qs ? '?' + qs : ''}`)
    },
    get: (id) => request('GET', `/tasks/${id}`),
    update: (id, updates) => request('PATCH', `/tasks/${id}`, updates),
    delete: (id) => request('DELETE', `/tasks/${id}`),
  },
}
