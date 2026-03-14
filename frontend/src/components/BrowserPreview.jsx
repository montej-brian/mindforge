/**
 * BrowserPreview — Real-time browser state visualization
 */
import useStore from '../store/useStore'
import './BrowserPreview.css'

export default function BrowserPreview() {
  const currentUrl   = useStore((s) => s.currentUrl)
  const screenshotUrl = useStore((s) => s.screenshotUrl)

  return (
    <div className="browser-preview glass-card panel">
      <div className="panel-header">
        <span className="panel-title">Browser View</span>
        <span className="tag">{currentUrl || 'No active session'}</span>
      </div>

      <div className="preview-viewport">
        {screenshotUrl ? (
          <img
            id="browser-screenshot"
            src={screenshotUrl}
            alt="Current browser state"
            className="screenshot-img"
          />
        ) : (
          <div className="preview-placeholder">
            <span className="preview-icon">🌐</span>
            <p>Browser session inactive</p>
            <p className="preview-hint">Agent will display screenshots here when active</p>
          </div>
        )}
      </div>
    </div>
  )
}
