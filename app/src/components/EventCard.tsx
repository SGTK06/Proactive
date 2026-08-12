import React from 'react'
import type { CalendarEvent } from '../types/calendar'

interface EventCardProps {
  event: CalendarEvent
}

/**
 * Reusable EventCard component for rendering individual Google Calendar tasks / schedule items.
 */
export const EventCard: React.FC<EventCardProps> = ({ event }) => {
  // Format event start time or date
  const startTime = event.start.dateTime
    ? new Date(event.start.dateTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : 'All Day'

  const startDate = event.start.dateTime
    ? new Date(event.start.dateTime).toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' })
    : event.start.date || ''

  return (
    <div className="event-card">
      <div className="event-header">
        <span className="event-title">{event.summary || 'Untitled Task'}</span>
        <span className="event-badge">{startTime}</span>
      </div>
      <div className="event-meta">
        <span className="event-date">📅 {startDate}</span>
        {event.location && <span className="event-location">📍 {event.location}</span>}
      </div>
      {event.description && <p className="event-desc">{event.description}</p>}
    </div>
  )
}
