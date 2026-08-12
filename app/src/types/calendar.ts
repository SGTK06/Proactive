export interface CalendarEvent {
  id: string
  summary: string
  description?: string
  location?: string
  start: {
    dateTime?: string
    date?: string
  }
  end: {
    dateTime?: string
    date?: string
  }
}

export interface UserProfile {
  name: string
  email: string
  picture?: string
  access_token?: string
}
