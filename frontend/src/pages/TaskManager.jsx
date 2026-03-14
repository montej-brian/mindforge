/**
 * TaskManager — Full task queue management page
 */
import TaskQueue from '../components/TaskQueue'

export default function TaskManager() {
  return (
    <div className="fade-in">
      <div className="page-header">
        <h1 className="page-title">📋 Task Manager</h1>
        <p className="page-subtitle">Create, manage, and monitor assignment automation tasks</p>
      </div>
      <div style={{ maxWidth: 720 }}>
        <TaskQueue />
      </div>
    </div>
  )
}
