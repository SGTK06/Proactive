import { useState, useEffect } from 'react'
import './App.css'
import type { UserProfile, CalendarEvent } from './types/calendar'
import { UserHeader } from './components/UserHeader'
import { ScheduleView } from './components/ScheduleView'

function App() {
  // Load saved user session from localStorage
  const [user, setUser] = useState<UserProfile | null>(() => {
    const savedUser = localStorage.getItem('proactive_user_session')
    return savedUser ? JSON.parse(savedUser) : null
  })

  const [events, setEvents] = useState<CalendarEvent[]>([])
  const [loading, setLoading] = useState<boolean>(false)

  // Parse Google OAuth redirect URL parameters on initial load
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const userParam = params.get('user')

    if (userParam) {
      try {
        const parsedUser: UserProfile = JSON.parse(userParam)
        setUser(parsedUser)
        // Store authenticated session
        localStorage.setItem('proactive_user_session', JSON.stringify(parsedUser))
        // Clean URL query parameters
        window.history.replaceState({}, document.title, window.location.pathname)
      } catch (err) {
        console.error('Failed to parse authenticated user profile:', err)
      }
    }
  }, [])

  // Automatically fetch Google Calendar events when user session is available
  useEffect(() => {
    if (user?.access_token) {
      fetchGoogleCalendarEvents(user.access_token)
    }
  }, [user])

  // Fetch current week's schedule events from FastAPI backend
  const fetchGoogleCalendarEvents = async (accessToken: string) => {
    setLoading(true)
    try {
      const res = await fetch(`http://localhost:8000/api/calendar/events?access_token=${encodeURIComponent(accessToken)}`)
      if (res.ok) {
        const data = await res.json()
        setEvents(data)
      } else {
        console.warn('Failed to fetch events from backend proxy')
      }
    } catch (err) {
      console.error('Error connecting to calendar endpoint:', err)
    } finally {
      setLoading(false)
    }
  }

  // Trigger Google OAuth 2.0 via FastAPI backend endpoint
  const handleGoogleLogin = () => {
    window.location.href = 'http://localhost:8000/api/auth/google/login'
  }

  // Clear session on sign out
  const handleLogout = () => {
    localStorage.removeItem('proactive_user_session')
    setUser(null)
    setEvents([])
  }

  return (
    <div className="whiteboard-container">
      {/* Decorative Whiteboard Sticky Notes */}
      <div className="sticky-note sticky-note-1">
        📌 <strong>Today's Focus:</strong> Seamless productivity
      </div>
      <div className="sticky-note sticky-note-2">
        💡 <strong>Proactive:</strong> Intelligent workspace
      </div>

      {/* Brand Header */}
      <div className="app-badge">
        <span className="badge-dot"></span>
        Proactive Workspace
      </div>

      <h1 className="main-title">Focus & Organize</h1>
      <p className="subtitle">
        A minimalist productivity workspace designed to keep your focus on what matters most.
      </p>

      {/* Main Whiteboard Card */}
      <div className={`whiteboard-card ${user ? 'card-expanded' : ''}`}>
        {user ? (
          /* Logged-in Homepage View with Google Calendar Schedule */
          <div className="workspace-view">
            <UserHeader user={user} onLogout={handleLogout} />
            <ScheduleView
              events={events}
              loading={loading}
              onFetchEvents={() => user.access_token && fetchGoogleCalendarEvents(user.access_token)}
            />
          </div>
        ) : (
          /* Clean Production Login State */
          <div>
            <div className="card-header">
              <h2>Welcome Back</h2>
              <p>Sign in to access your whiteboard workspace</p>
            </div>

            <div className="auth-actions">
              <button className="google-btn" onClick={handleGoogleLogin}>
                <svg className="google-icon" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                  />
                </svg>
                Continue with Google
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
