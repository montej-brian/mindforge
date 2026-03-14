/**
 * TaskQueue — Assignment task queue display + add task form
 */
import { useState, useEffect } from 'react'
import useStore from '../store/useStore'
import { api } from '../services/api'
import './TaskQueue.css'

const STATUS_BADGE = {
  pending:   'badge-pending',
  running:   'badge-running',
  completed: 'badge-done',
  failed:    'badge-failed',
}

export default function TaskQueue() {
  const { tasks, setTasks, addTask, removeTask } = useStore()
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', instructions: '', target_url: '', priority: 'normal' })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.tasks.list().then(setTasks).catch(console.warn)
  }, [setTasks])

  async function handleCreate(e) {
    e.preventDefault()
    setLoading(true)
    try {
      const task = await api.tasks.create(form)
      addTask(task)
      setForm({ title: '', instructions: '', target_url: '', priority: 'normal' })
      setShowForm(false)
    } catch (err) {
      alert(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete(id) {
    await api.tasks.delete(id).catch(console.warn)
    removeTask(id)
  }

  return (
    <div className="task-queue glass-card panel">
      <div className="panel-header">
        <span className="panel-title">Task Queue</span>
        <button id="add-task-btn" className="btn btn-primary" style={{ padding: '6px 14px', fontSize: 12 }} onClick={() => setShowForm(!showForm)}>
          {showForm ? '✕ Cancel' : '+ Add Task'}
        </button>
      </div>

      {showForm && (
        <form className="task-form fade-in" onSubmit={handleCreate}>
          <input id="task-title" className="input" placeholder="Task title" value={form.title}
            onChange={e => setForm(f => ({ ...f, title: e.target.value }))} required />
          <input id="task-url" className="input" placeholder="Target URL (optional)" value={form.target_url}
            onChange={e => setForm(f => ({ ...f, target_url: e.target.value }))} />
          <textarea id="task-instructions" className="input" placeholder="Instructions…" rows={3} value={form.instructions}
            onChange={e => setForm(f => ({ ...f, instructions: e.target.value }))} required />
          <select id="task-priority" className="input" value={form.priority}
            onChange={e => setForm(f => ({ ...f, priority: e.target.value }))}>
            <option value="high">High Priority</option>
            <option value="normal">Normal Priority</option>
            <option value="low">Low Priority</option>
          </select>
          <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%' }}>
            {loading ? 'Creating…' : 'Create Task'}
          </button>
        </form>
      )}

      <div className="task-list">
        {tasks.length === 0 && (
          <p className="empty-state">No tasks yet. Add one or use voice control.</p>
        )}
        {tasks.map((task) => (
          <div key={task.id} className="task-item fade-in" id={`task-${task.id}`}>
            <div className="task-item-header">
              <span className="task-title">{task.title}</span>
              <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                <span className={`badge ${STATUS_BADGE[task.status] || 'badge-pending'}`}>{task.status}</span>
                <button className="btn btn-ghost" style={{ padding: '3px 8px', fontSize: 11 }}
                  onClick={() => handleDelete(task.id)}>✕</button>
              </div>
            </div>
            {task.target_url && <span className="tag">{task.target_url}</span>}
            <p className="task-instructions">{task.instructions}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
