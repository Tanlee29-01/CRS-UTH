import { useState, useMemo } from "react";
import Calendar from "./Calendar.jsx";
import DonutChart from "./DonutChart.jsx";
import EmptyState from "./EmptyState.jsx";

const QUICK_ACTIONS = [
  { icon: "🎓", label: "Đào tạo trực tuyến", route: "catalog" },
  { icon: "💬", label: "Hỗ trợ trực tuyến", route: null },
  { icon: "🏦", label: "Thanh toán trực tuyến", route: null },
  { icon: "💰", label: "Thanh toán khoản thu khác", route: null },
  { icon: "📋", label: "Chương trình khung", route: null },
  { icon: "📊", label: "Kết quả học tập", route: null },
  { icon: "📝", label: "Dịch vụ sinh viên", route: null },
];

function KV({ label, value }) {
  return (
    <>
      <div className="kv-label">{label}:</div>
      <div className="kv-value">{value || "—"}</div>
    </>
  );
}

export default function Dashboard({
  profile, enrollments, courses, sections, terms, notifications,
  meetingTimes, onTabChange
}) {
  const student = profile?.student;
  const [selectedSemester, setSelectedSemester] = useState("");

  const enrolledCourses = useMemo(() => {
    return enrollments.map((e) => {
      const section = sections.find((s) => s.id === e.section_id);
      const course = section ? courses.find((c) => c.id === section.course_id) : null;
      return {
        id: e.id,
        courseName: course ? course.title : "—",
        courseCode: course ? course.code : "",
        credits: course ? course.credits_max : 0,
        sectionNumber: section?.section_number || "—",
      };
    });
  }, [enrollments, sections, courses]);

  const achievedCredits = useMemo(() => {
    return enrolledCourses.reduce((sum, c) => sum + c.credits, 0);
  }, [enrolledCourses]);

  const totalCredits = 120;
  const reminderCount = notifications?.length || 0;
  const weeklyCount = enrollments?.length || 0;

  const levelText = student?.level === "undergrad" ? "Đại học - chính quy" : student?.level || "—";

  return (
    <div className="dashboard">
      {/* Row 1: Student Info + Calendar */}
      <div className="dash-row dash-row-top">
        <div className="card student-card">
          <div className="card-header">
            <span className="card-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              Thông tin sinh viên
            </span>
            <span className="card-badge">THẺ SINH VIÊN</span>
          </div>
          <div className="card-body student-body">
            <div className="student-avatar-col">
              <div className="student-avatar">
                {profile?.email?.[0]?.toUpperCase() || "S"}
              </div>
            </div>
            <div className="student-info-col">
              <div className="kv-grid">
                <KV label="MSSV" value={student?.student_number} />
                <KV label="Khóa học" value="2024" />
                <KV label="Họ tên" value={profile?.email?.split("@")[0]?.replace(/\./g, " ") || "—"} />
                <KV label="Giới tính" value="—" />
                <KV label="Ngày sinh" value="—" />
                <KV label="Bậc đào tạo" value={levelText} />
                <KV label="Nơi sinh" value="—" />
                <KV label="Loại hình đào tạo" value="Tiên tiến" />
                <KV label="Ngành" value="Công nghệ thông tin" />
                <KV label="Chuyên ngành" value={student?.major || "Khoa học dữ liệu và AI"} />
              </div>
            </div>
          </div>
        </div>

        <div className="card calendar-card">
          <div className="card-header">
            <span className="card-title">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
              Lịch theo tháng
            </span>
          </div>
          <div className="card-body">
            <Calendar />
          </div>
        </div>
      </div>

      {/* Row 2: Stats */}
      <div className="dash-row dash-row-stats">
        <div className="card stat-card">
          <div className="stat-content">
            <div className="stat-info">
              <div className="stat-label">Nhắc nhở</div>
              <div className="stat-number">{reminderCount}</div>
              <a href="#" className="stat-link" onClick={(e) => { e.preventDefault(); onTabChange?.("catalog"); }}>Xem chi tiết</a>
            </div>
            <div className="stat-icon-wrap">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#f39c12" strokeWidth="2"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0"/></svg>
            </div>
          </div>
        </div>
        <div className="card stat-card stat-teal">
          <div className="stat-content">
            <div className="stat-info">
              <div className="stat-label">Lịch học trong tuần</div>
              <div className="stat-number">{weeklyCount}</div>
              <a href="#" className="stat-link" onClick={(e) => { e.preventDefault(); onTabChange?.("catalog"); }}>Xem chi tiết</a>
            </div>
            <div className="stat-icon-wrap">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
            </div>
          </div>
        </div>
      </div>

      {/* Row 3: Quick Actions */}
      <div className="dash-row">
        <div className="quick-actions">
          {QUICK_ACTIONS.map((qa, i) => (
            <button
              key={i}
              className="qa-tile"
              onClick={() => qa.route && onTabChange?.(qa.route)}
            >
              <div className="qa-icon-wrap">
                <span className="qa-icon">{qa.icon}</span>
              </div>
              <div className="qa-label">{qa.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Row 4: Bottom cards */}
      <div className="dash-row dash-row-bottom">
        <div className="card">
          <div className="card-header">
            <span className="card-title">Kết quả học tập</span>
            <select
              className="semester-select"
              value={selectedSemester}
              onChange={(e) => setSelectedSemester(e.target.value)}
            >
              <option value="">Chọn học kỳ</option>
              {terms.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
          </div>
          <div className="card-body">
            <EmptyState icon="📝" message="Không có dữ liệu cho học kỳ này!" />
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <span className="card-title">Tiến độ học tập</span>
          </div>
          <div className="card-body donut-body">
            <DonutChart achieved={achievedCredits} total={totalCredits} />
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <span className="card-title">Lớp học phần</span>
            <select
              className="semester-select"
              value={selectedSemester}
              onChange={(e) => setSelectedSemester(e.target.value)}
            >
              <option value="">Chọn học kỳ</option>
              {terms.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
          </div>
          <div className="card-body">
            {enrolledCourses.length === 0 ? (
              <EmptyState icon="📚" message="Chưa đăng ký học phần nào" />
            ) : (
              <div className="course-table-wrap">
                <table className="course-table">
                  <thead>
                    <tr>
                      <th>Môn học</th>
                      <th className="text-center">Tín chỉ</th>
                    </tr>
                  </thead>
                  <tbody>
                    {enrolledCourses.map((c) => (
                      <tr key={c.id}>
                        <td className={c.credits >= 4 ? "highlight" : ""}>{c.courseName}</td>
                        <td className="text-center">{c.credits}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
