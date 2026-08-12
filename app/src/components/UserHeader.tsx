import React from 'react'
import type { UserProfile } from '../types/calendar'

interface UserHeaderProps {
  user: UserProfile
  onLogout: () => void
}

/**
 * Reusable UserHeader component for displaying user avatar, name, email, and logout button.
 */
export const UserHeader: React.FC<UserHeaderProps> = ({ user, onLogout }) => {
  return (
    <div className="profile-box">
      {user.picture && <img src={user.picture} alt={user.name} className="avatar" />}
      <div>
        <div className="user-name">{user.name}</div>
        <div className="user-email">{user.email}</div>
      </div>
      <button className="logout-btn" onClick={onLogout}>
        Sign Out
      </button>
    </div>
  )
}
