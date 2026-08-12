import React from 'react'
import type { CalendarEvent } from '../types/calendar'
import { EventCard } from './EventCard'

interface ScheduleViewProps {
  events: CalendarEvent[]
  loading: boolean
  onFetchEvents: () => void
}

/**
 * Reusable ScheduleView component for rendering weekly task schedule on the homepage.
 */
export const ScheduleView: React.FC<ScheduleViewProps> = ({ events, loading, onFetchEvents }) => {
  return (
    <div className="schedule-section">
      <div className="schedule-header">
        <h3>📅 Week's Schedule</h3>
        <button className="sync-btn" onClick={onFetchEvents} disabled={loading}>
          {loading ? 'Syncing...' : '🔄 Sync Google Calendar'}
        </button>
      </div>

      {loading ? (
        <div className="empty-schedule">
          <p>Importing your Google Calendar schedule...</p>
        </div>
      ) : events.length > 0 ? (
        <div className="events-grid">
          {events.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      ) : (
        <div className="empty-schedule">
          <p>No upcoming Google Calendar tasks found for this week.</p>
          <button className="sync-btn" onClick={onFetchEvents} style={{ marginTop: '0.5rem' }}>
            Import Schedule
          </button>
        </div>
      )}
    </div>
  )
}
