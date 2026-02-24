import { useState } from "react";

export default function Header({ profile, onLogout }) {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <header className="uth-header">
      <div className="header-left">
        <button className="hamburger" aria-label="Menu">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M3 12h18M3 6h18M3 18h18" />
          </svg>
        </button>
        <div className="uth-logo">
          <span className="logo-text">UTH</span>
          <div className="logo-sub">
            <span>UNIVERSITY OF TRANSPORT</span>
            <span>HOCHIMINH CITY</span>
          </div>
        </div>
      </div>

      {profile && (
        <div className="header-right">
          <div className="user-menu" onClick={() => setDropdownOpen(!dropdownOpen)}>
            <div className="user-avatar">
              {profile.email?.[0]?.toUpperCase() || "U"}
            </div>
            <span className="user-name">{profile.email?.split("@")[0] || profile.email}</span>
            <span className="user-caret">▾</span>
          </div>
          {dropdownOpen && (
            <>
              <div className="dropdown-overlay" onClick={() => setDropdownOpen(false)} />
              <div className="user-dropdown">
                <div className="dropdown-info">
                  <div className="dropdown-role">{profile.role?.toUpperCase()}</div>
                  {profile.student && (
                    <div className="dropdown-id">MSSV: {profile.student.student_number}</div>
                  )}
                </div>
                <div className="dropdown-divider" />
                <button className="dropdown-item" onClick={() => { onLogout(); setDropdownOpen(false); }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
                  </svg>
                  Đăng xuất
                </button>
              </div>
            </>
          )}
        </div>
      )}
    </header>
  );
}
