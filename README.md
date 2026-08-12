# Proactive

**Intelligent Personal Productivity Tool**

_Intelligent Task Planner That Schedules Tasks Realistically_

Proactive factors work hours, commute time, and task priority and duration into consideration before planning tasks for the day. Tasks can be broken down/split across two days and the backlogs are maintained by the system.

**Features:**

1. Access to Google Calendar so that the scheduled tasks do not overlap with existing ones.
2. Access to Google Maps API for getting accurate estimates of travel time, and dynamically reschedule to accomodate any unnecessary delays.
3. Task prioritization based on importance, deadline, and other metrics.
4. Set custom reminders for tasks.

**Future Extensions:**

1. Effort as a core metric to decide daily task allocation (Each day has tasks with same average difficulty to avoid overloading).
2. Task input through Google Calendar or Proactive Web UI

## Product

The core management and smart task rescheduling logic is handled by the web app running dynamic rescheduling. For seamless integration and user experience, the web app will manage Google Calendar and schedule reminders through Google Calendar.

## Deployment

This repository is configured for Vercel with a Vite frontend in `app/` and a FastAPI serverless entrypoint in `api/index.py`.

Set these environment variables in Vercel:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `REDIRECT_URI`, for example `https://your-domain.vercel.app/api/auth/google/callback`
- `FRONTEND_URL`, for example `https://your-domain.vercel.app`

For local development:

- Frontend: `cd app && npm install && npm run dev`
- Backend: `pip install -r requirements.txt && python -m uvicorn backend.main:app --reload`
