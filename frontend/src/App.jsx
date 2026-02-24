import { useEffect, useState } from "react";
import { apiDelete, apiGet, apiPost } from "./api/client.js";
import Header from "./components/Header.jsx";
import LoginPage from "./components/LoginPage.jsx";
import Dashboard from "./components/Dashboard.jsx";
import CatalogPanel from "./components/CatalogPanel.jsx";
import AdminPanel from "./components/AdminPanel.jsx";

export default function App() {
  /* ===== Auth ===== */
  const [token, setToken] = useState("");
  const [profile, setProfile] = useState(null);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [authMessage, setAuthMessage] = useState("");

  /* ===== Catalog ===== */
  const [departments, setDepartments] = useState([]);
  const [courses, setCourses] = useState([]);
  const [terms, setTerms] = useState([]);
  const [sections, setSections] = useState([]);
  const [selectedTerm, setSelectedTerm] = useState("");
  const [selectedCourse, setSelectedCourse] = useState("");

  /* ===== Enrollment ===== */
  const [enrollments, setEnrollments] = useState([]);
  const [meetingTimes, setMeetingTimes] = useState({});
  const [cart, setCart] = useState([]);
  const [cartMessage, setCartMessage] = useState("");

  /* ===== Admin ===== */
  const [adminMessage, setAdminMessage] = useState("");
  const [adminDepartment, setAdminDepartment] = useState({ code: "", name: "" });
  const [adminCourse, setAdminCourse] = useState({
    code: "", title: "", description: "", credits_min: 3, credits_max: 3, level: 100, department_id: ""
  });
  const [adminTerm, setAdminTerm] = useState({
    code: "", name: "", start_date: "2026-01-12", end_date: "2026-05-15",
    registration_open: "2026-01-02", registration_close: "2026-02-15", add_drop_deadline: "2026-02-01"
  });
  const [adminSection, setAdminSection] = useState({
    term_id: "", course_id: "", section_number: "001", capacity: 30, waitlist_capacity: 5,
    delivery_mode: "in_person", location: "Bldg A", status: "open"
  });
  const [adminMeeting, setAdminMeeting] = useState({
    section_id: "", day_of_week: "Mon", start_time: "09:00:00", end_time: "10:15:00"
  });
  const [adminRule, setAdminRule] = useState({
    course_id: "", rule_type: "prereq", rule_data: '{"course_codes":["CS101"]}', active: true
  });
  const [rules, setRules] = useState([]);
  const [adminEnrollments, setAdminEnrollments] = useState([]);
  const [students, setStudents] = useState([]);
  const [csvText, setCsvText] = useState("");
  const [csvTarget, setCsvTarget] = useState("departments");
  const [instructorSectionId, setInstructorSectionId] = useState("");
  const [roster, setRoster] = useState([]);
  const [reports, setReports] = useState([]);
  const [reportTerm, setReportTerm] = useState("");
  const [reportCourse, setReportCourse] = useState("");
  const [notifications, setNotifications] = useState([]);

  /* ========== Effects ========== */

  // Load catalog data on mount
  useEffect(() => {
    apiGet("/departments").then(setDepartments).catch(() => {});
    apiGet("/courses").then(setCourses).catch(() => {});
    apiGet("/terms").then(setTerms).catch(() => {});
  }, []);

  // Load sections when filters change
  useEffect(() => {
    const p = new URLSearchParams();
    if (selectedTerm) p.set("term_id", selectedTerm);
    if (selectedCourse) p.set("course_id", selectedCourse);
    apiGet(`/sections${p.toString() ? "?" + p : ""}`)
      .then(setSections).catch(() => setSections([]));
  }, [selectedTerm, selectedCourse]);

  // Load enrollments, profile, notifications when logged in
  useEffect(() => {
    if (!token) return;
    apiGet("/me/enrollments", token).then(setEnrollments).catch(() => setEnrollments([]));
    apiGet("/auth/me/profile", token).then(setProfile).catch(() => setProfile(null));
    apiGet("/notifications", token).then(setNotifications).catch(() => setNotifications([]));
  }, [token]);

  // Load meeting times for enrolled + cart sections
  useEffect(() => {
    const ids = new Set([...enrollments.map((e) => e.section_id), ...cart]);
    ids.forEach(async (id) => {
      if (meetingTimes[id]) return;
      try {
        const data = await apiGet(`/sections/${id}/meeting-times`);
        setMeetingTimes((prev) => ({ ...prev, [id]: data }));
      } catch {
        setMeetingTimes((prev) => ({ ...prev, [id]: [] }));
      }
    });
  }, [enrollments, cart]);

  /* ========== Handlers ========== */

  async function handleLogin(email, password, mode) {
    setAuthMessage("");
    try {
      if (mode === "register") {
        await apiPost("/auth/register", { email, password, role: "student" });
      }
      const data = await apiPost("/auth/login", { email, password });
      setToken(data.access_token);
    } catch {
      setAuthMessage("Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin.");
    }
  }

  function handleLogout() {
    setToken("");
    setProfile(null);
    setEnrollments([]);
    setNotifications([]);
    setMeetingTimes({});
    setCart([]);
    setActiveTab("dashboard");
  }

  async function handleEnroll(sectionId) {
    setAuthMessage("");
    try {
      await apiPost(`/sections/${sectionId}/enroll`, {}, token);
      const latest = await apiGet("/me/enrollments", token);
      setEnrollments(latest);
      setCart((prev) => prev.filter((id) => id !== sectionId));
      setAuthMessage("Đăng ký thành công ✓");
    } catch {
      setAuthMessage("Đăng ký thất bại hoặc đã vào danh sách chờ");
    }
  }

  async function handleDrop(sectionId) {
    setAuthMessage("");
    try {
      await apiPost(`/sections/${sectionId}/drop`, {}, token);
      const latest = await apiGet("/me/enrollments", token);
      setEnrollments(latest);
      setAuthMessage("Đã hủy đăng ký ✓");
    } catch {
      setAuthMessage("Hủy đăng ký thất bại");
    }
  }

  function addToCart(id) { if (!cart.includes(id)) setCart([...cart, id]); }
  function removeFromCart(id) { setCart(cart.filter((x) => x !== id)); }

  async function validateCart() {
    try {
      const res = await apiPost("/cart/validate", { section_ids: cart }, token);
      setCartMessage(res.ok ? "Giỏ đăng ký hợp lệ ✓" : res.errors.join("; "));
    } catch { setCartMessage("Kiểm tra thất bại"); }
  }

  async function estimateBill() {
    try {
      const res = await apiPost("/billing/estimate", { section_ids: cart }, token);
      setCartMessage(`Ước tính: ${res.total.toLocaleString()}đ (${res.credits} tín chỉ)`);
    } catch { setCartMessage("Ước tính thất bại"); }
  }

  async function handleAdminCreate(path, payload, method = "post") {
    setAdminMessage("");
    try {
      if (method === "delete") await apiDelete(path, token);
      else await apiPost(path, payload, token);
      setAdminMessage("Thành công ✓");
      // Refresh catalog data
      const [deps, crs, trs] = await Promise.all([
        apiGet("/departments"), apiGet("/courses"), apiGet("/terms")
      ]);
      setDepartments(deps); setCourses(crs); setTerms(trs);
      const p = new URLSearchParams();
      if (selectedTerm) p.set("term_id", selectedTerm);
      if (selectedCourse) p.set("course_id", selectedCourse);
      setSections(await apiGet(`/sections${p.toString() ? "?" + p : ""}`));
    } catch { setAdminMessage("Thao tác thất bại"); }
  }

  async function refreshAdminLists() {
    try {
      const [r, e, s] = await Promise.all([
        apiGet("/admin/rules", token),
        apiGet("/admin/enrollments", token),
        apiGet("/admin/students", token)
      ]);
      setRules(r); setAdminEnrollments(e); setStudents(s);
    } catch { setRules([]); setAdminEnrollments([]); setStudents([]); }
  }

  async function fetchReports() {
    try {
      const p = new URLSearchParams();
      if (reportTerm) p.set("term_id", reportTerm);
      if (reportCourse) p.set("course_id", reportCourse);
      setReports(await apiGet(`/admin/reports/sections${p.toString() ? "?" + p : ""}`, token));
    } catch { setReports([]); }
  }

  async function fetchRoster() {
    try {
      setRoster(await apiGet(`/instructor/sections/${instructorSectionId}/roster`, token));
    } catch { setRoster([]); }
  }

  async function fetchNotifications() {
    try { setNotifications(await apiGet("/notifications", token)); }
    catch { setNotifications([]); }
  }

  /* ========== Render ========== */

  if (!token) {
    return (
      <>
        <Header profile={null} onLogout={handleLogout} />
        <LoginPage onLogin={handleLogin} errorMessage={authMessage} />
      </>
    );
  }

  const tabs = [
    { id: "dashboard", label: "Trang chủ", icon: "🏠" },
    { id: "catalog", label: "Đăng ký học phần", icon: "📚" },
  ];
  if (profile?.role === "admin" || profile?.role === "registrar") {
    tabs.push({ id: "admin", label: "Quản trị", icon: "⚙️" });
  }

  return (
    <>
      <Header profile={profile} onLogout={handleLogout} />
      <nav className="nav-tabs">
        {tabs.map((t) => (
          <button
            key={t.id}
            className={`nav-tab ${activeTab === t.id ? "active" : ""}`}
            onClick={() => setActiveTab(t.id)}
          >
            <span className="nav-tab-icon">{t.icon}</span>
            {t.label}
          </button>
        ))}
      </nav>
      <main className="main-content">
        {activeTab === "dashboard" && (
          <Dashboard
            profile={profile}
            enrollments={enrollments}
            courses={courses}
            sections={sections}
            terms={terms}
            notifications={notifications}
            meetingTimes={meetingTimes}
            onTabChange={setActiveTab}
          />
        )}
        {activeTab === "catalog" && (
          <CatalogPanel
            courses={courses} sections={sections} terms={terms} departments={departments}
            selectedTerm={selectedTerm} setSelectedTerm={setSelectedTerm}
            selectedCourse={selectedCourse} setSelectedCourse={setSelectedCourse}
            enrollments={enrollments} token={token}
            onEnroll={handleEnroll} onDrop={handleDrop}
            cart={cart} onAddToCart={addToCart} onRemoveFromCart={removeFromCart}
            onValidateCart={validateCart} onEstimateBill={estimateBill} cartMessage={cartMessage}
            meetingTimes={meetingTimes} authMessage={authMessage}
          />
        )}
        {activeTab === "admin" && (
          <AdminPanel
            token={token} courses={courses} terms={terms} departments={departments} sections={sections}
            adminMessage={adminMessage}
            adminDepartment={adminDepartment} setAdminDepartment={setAdminDepartment}
            adminCourse={adminCourse} setAdminCourse={setAdminCourse}
            adminTerm={adminTerm} setAdminTerm={setAdminTerm}
            adminSection={adminSection} setAdminSection={setAdminSection}
            adminMeeting={adminMeeting} setAdminMeeting={setAdminMeeting}
            adminRule={adminRule} setAdminRule={setAdminRule}
            rules={rules} adminEnrollments={adminEnrollments} students={students}
            reports={reports} reportTerm={reportTerm} setReportTerm={setReportTerm}
            reportCourse={reportCourse} setReportCourse={setReportCourse}
            instructorSectionId={instructorSectionId} setInstructorSectionId={setInstructorSectionId}
            roster={roster}
            csvText={csvText} setCsvText={setCsvText} csvTarget={csvTarget} setCsvTarget={setCsvTarget}
            onAdminCreate={handleAdminCreate} onRefreshLists={refreshAdminLists}
            onFetchReports={fetchReports} onFetchRoster={fetchRoster}
            notifications={notifications} onFetchNotifications={fetchNotifications}
          />
        )}
      </main>
    </>
  );
}
