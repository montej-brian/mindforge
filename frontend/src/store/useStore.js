/**
 * MINDFORGE — Zustand Global State Store
 */
import { create } from 'zustand'

const useStore = create((set, get) => ({
  // ─── Connection State ────────────────────────────────────────────────────
  wsConnected: false,
  setWsConnected: (connected) => set({ wsConnected: connected }),

  // ─── Voice State ─────────────────────────────────────────────────────────
  isListening: false,
  voiceTranscript: '',
  setListening: (isListening) => set({ isListening }),
  setTranscript: (voiceTranscript) => set({ voiceTranscript }),

  // ─── Agent State ─────────────────────────────────────────────────────────
  agents: {
    orchestrator: { status: 'idle', message: '' },
    browser:      { status: 'idle', message: '' },
    voice:        { status: 'idle', message: '' },
    assignment:   { status: 'idle', message: '' },
  },
  updateAgent: (agentName, update) =>
    set((state) => ({
      agents: { ...state.agents, [agentName]: { ...state.agents[agentName], ...update } },
    })),

  // ─── Task Queue ───────────────────────────────────────────────────────────
  tasks: [],
  setTasks: (tasks) => set({ tasks }),
  addTask: (task) => set((state) => ({ tasks: [task, ...state.tasks] })),
  updateTask: (id, update) =>
    set((state) => ({
      tasks: state.tasks.map((t) => (t.id === id ? { ...t, ...update } : t)),
    })),
  removeTask: (id) => set((state) => ({ tasks: state.tasks.filter((t) => t.id !== id) })),

  // ─── Event Log ────────────────────────────────────────────────────────────
  events: [],
  addEvent: (event) =>
    set((state) => ({
      events: [{ ...event, id: Date.now(), timestamp: new Date().toISOString() }, ...state.events].slice(0, 100),
    })),
  clearEvents: () => set({ events: [] }),

  // ─── Browser Preview ──────────────────────────────────────────────────────
  currentUrl: '',
  screenshotUrl: '',
  setCurrentUrl: (currentUrl) => set({ currentUrl }),
  setScreenshotUrl: (screenshotUrl) => set({ screenshotUrl }),
}))

export default useStore
