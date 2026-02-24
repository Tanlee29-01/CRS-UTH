import { useState } from "react";

const ANNOUNCEMENTS = [
  { title: "Thông báo về việc đăng ký học phần học kỳ 2 năm học 2025-2026 (Bổ sung)", date: "05/02/2026" },
  { title: "Thông báo Điều chỉnh đăng ký học phần học kỳ 2 năm học 2025-2026", date: "23/01/2026" },
  { title: "THÔNG BÁO Về điều kiện sinh viên tham gia xét học bổng khuyến khích học tập UTH học kỳ 1, năm học 2024-2025", date: "20/01/2026" },
  { title: "THÔNG BÁO về việc đóng bảo hiểm y tế sinh viên đợt 2 năm 2025-2026", date: "13/01/2026" },
  { title: "THÔNG BÁO Về việc xét học vụ năm học 2024 - 2025", date: "31/12/2025" },
  { title: "THÔNG BÁO về việc đăng ký học phần học kỳ 2 năm học 2025-2026 (Đợt 1)", date: "10/12/2025" },
];

const TABS = ["THÔNG BÁO CHUNG", "CTCT- QL SINH VIÊN", "THÔNG TIN ĐÀO TẠO", "ĐÀO T..."];

export default function LoginPage({ onLogin, errorMessage }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState("login");
  const [showPw, setShowPw] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  function handleSubmit(e) {
    e.preventDefault();
    onLogin(email, password, mode);
  }

  return (
    <div className="login-page">
      <div className="login-bg">
        <div className="login-watermark">UTH</div>
        <div className="login-watermark login-watermark-2">UTH</div>
      </div>
      <div className="login-content">
        <div className="login-left">
          <div className="announce-card">
            <div className="announce-tabs">
              {TABS.map((t, i) => (
                <button
                  key={i}
                  className={`announce-tab ${i === activeTab ? "active" : ""}`}
                  onClick={() => setActiveTab(i)}
                >
                  {t}
                </button>
              ))}
            </div>
            <ul className="announce-list">
              {ANNOUNCEMENTS.map((a, i) => (
                <li key={i} className="announce-item">
                  <div className="announce-title">{a.title}</div>
                  <div className="announce-meta">
                    <span className="announce-date">{a.date}</span>
                    <a href="#" className="announce-link">Xem chi tiết</a>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="login-right">
          <div className="login-form-card">
            <div className="login-logo">
              <div className="login-logo-icon">
                <span className="logo-text-lg">UTH</span>
              </div>
              <div className="login-logo-sub">
                UNIVERSITY<br />OF TRANSPORT<br />HOCHIMINH CITY
              </div>
            </div>
            <h2 className="login-heading">ĐĂNG NHẬP HỆ THỐNG</h2>
            <form onSubmit={handleSubmit} className="login-form">
              <div className="form-group">
                <input
                  type="email"
                  placeholder="Tài khoản đăng nhập"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoComplete="email"
                />
              </div>
              <div className="form-group password-group">
                <input
                  type={showPw ? "text" : "password"}
                  placeholder="Mật khẩu"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoComplete="current-password"
                />
                <button type="button" className="eye-btn" onClick={() => setShowPw(!showPw)} tabIndex={-1}>
                  {showPw ? (
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#999" strokeWidth="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24M1 1l22 22"/></svg>
                  ) : (
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#999" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                  )}
                </button>
              </div>
              <button type="submit" className="btn-login">
                {mode === "login" ? "ĐĂNG NHẬP" : "ĐĂNG KÝ & ĐĂNG NHẬP"}
              </button>
            </form>
            {errorMessage && <div className="login-error">{errorMessage}</div>}
            <div className="login-links">
              <button className="link-switch" onClick={() => setMode(mode === "login" ? "register" : "login")}>
                {mode === "login" ? "Đăng ký tài khoản mới" : "Đã có tài khoản? Đăng nhập"}
              </button>
              {mode === "login" && <a href="#" className="link-forgot">Quên mật khẩu?</a>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
