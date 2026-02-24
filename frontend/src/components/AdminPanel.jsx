import { useState } from "react";

const ADMIN_TABS = [
  { id: "create", label: "Tạo mới" },
  { id: "lists", label: "Danh sách" },
  { id: "reports", label: "Báo cáo" },
  { id: "import", label: "Nhập CSV" },
  { id: "instructor", label: "Giảng viên" },
  { id: "notifications", label: "Thông báo" },
];

export default function AdminPanel({
  token,courses,terms,departments,sections,adminMessage,
  adminDepartment,setAdminDepartment,adminCourse,setAdminCourse,
  adminTerm,setAdminTerm,adminSection,setAdminSection,
  adminMeeting,setAdminMeeting,adminRule,setAdminRule,
  rules,adminEnrollments,students,
  reports,reportTerm,setReportTerm,reportCourse,setReportCourse,
  instructorSectionId,setInstructorSectionId,roster,
  csvText,setCsvText,csvTarget,setCsvTarget,
  onAdminCreate,onRefreshLists,onFetchReports,onFetchRoster,
  notifications,onFetchNotifications
}) {
  const [tab, setTab] = useState("create");

  return (
    <div className="admin-panel">
      <div className="admin-tabs">
        {ADMIN_TABS.map((t) => (
          <button key={t.id} className={`admin-tab ${tab === t.id ? "active" : ""}`} onClick={() => setTab(t.id)}>
            {t.label}
          </button>
        ))}
      </div>
      {adminMessage && <div className="toast-message">{adminMessage}</div>}

      {tab === "create" && (
        <div className="admin-create-grid">
          <FormCard title="Khoa" disabled={!token} onSubmit={() => onAdminCreate("/admin/departments",adminDepartment)}>
            <input placeholder="Mã khoa" value={adminDepartment.code} onChange={e=>setAdminDepartment({...adminDepartment,code:e.target.value})}/>
            <input placeholder="Tên khoa" value={adminDepartment.name} onChange={e=>setAdminDepartment({...adminDepartment,name:e.target.value})}/>
          </FormCard>
          <FormCard title="Môn học" disabled={!token} onSubmit={() => onAdminCreate("/admin/courses",adminCourse)}>
            <input placeholder="Mã môn" value={adminCourse.code} onChange={e=>setAdminCourse({...adminCourse,code:e.target.value})}/>
            <input placeholder="Tên môn" value={adminCourse.title} onChange={e=>setAdminCourse({...adminCourse,title:e.target.value})}/>
            <input placeholder="Mô tả" value={adminCourse.description} onChange={e=>setAdminCourse({...adminCourse,description:e.target.value})}/>
            <input placeholder="Department ID" type="number" value={adminCourse.department_id} onChange={e=>setAdminCourse({...adminCourse,department_id:Number(e.target.value)})}/>
          </FormCard>
          <FormCard title="Học kỳ" disabled={!token} onSubmit={() => onAdminCreate("/admin/terms",adminTerm)}>
            <input placeholder="Mã HK (2026SP)" value={adminTerm.code} onChange={e=>setAdminTerm({...adminTerm,code:e.target.value})}/>
            <input placeholder="Tên HK" value={adminTerm.name} onChange={e=>setAdminTerm({...adminTerm,name:e.target.value})}/>
            <input type="date" value={adminTerm.start_date} onChange={e=>setAdminTerm({...adminTerm,start_date:e.target.value})}/>
            <input type="date" value={adminTerm.end_date} onChange={e=>setAdminTerm({...adminTerm,end_date:e.target.value})}/>
            <input type="date" value={adminTerm.registration_open} onChange={e=>setAdminTerm({...adminTerm,registration_open:e.target.value})}/>
            <input type="date" value={adminTerm.registration_close} onChange={e=>setAdminTerm({...adminTerm,registration_close:e.target.value})}/>
            <input type="date" value={adminTerm.add_drop_deadline} onChange={e=>setAdminTerm({...adminTerm,add_drop_deadline:e.target.value})}/>
          </FormCard>
          <FormCard title="Lớp học phần" disabled={!token} onSubmit={() => onAdminCreate("/admin/sections",adminSection)}>
            <input placeholder="Term ID" type="number" value={adminSection.term_id} onChange={e=>setAdminSection({...adminSection,term_id:Number(e.target.value)})}/>
            <input placeholder="Course ID" type="number" value={adminSection.course_id} onChange={e=>setAdminSection({...adminSection,course_id:Number(e.target.value)})}/>
            <input placeholder="Số nhóm" value={adminSection.section_number} onChange={e=>setAdminSection({...adminSection,section_number:e.target.value})}/>
            <input placeholder="Sức chứa" type="number" value={adminSection.capacity} onChange={e=>setAdminSection({...adminSection,capacity:Number(e.target.value)})}/>
          </FormCard>
          <FormCard title="Lịch học" disabled={!token} onSubmit={() => onAdminCreate("/admin/meeting-times",adminMeeting)}>
            <input placeholder="Section ID" type="number" value={adminMeeting.section_id} onChange={e=>setAdminMeeting({...adminMeeting,section_id:Number(e.target.value)})}/>
            <input placeholder="Thứ (Mon/Tue...)" value={adminMeeting.day_of_week} onChange={e=>setAdminMeeting({...adminMeeting,day_of_week:e.target.value})}/>
            <input placeholder="Bắt đầu (09:00:00)" value={adminMeeting.start_time} onChange={e=>setAdminMeeting({...adminMeeting,start_time:e.target.value})}/>
            <input placeholder="Kết thúc (10:15:00)" value={adminMeeting.end_time} onChange={e=>setAdminMeeting({...adminMeeting,end_time:e.target.value})}/>
          </FormCard>
          <FormCard title="Quy tắc" disabled={!token} onSubmit={() => onAdminCreate("/admin/rules",adminRule)}>
            <input placeholder="Course ID (tùy chọn)" type="number" value={adminRule.course_id} onChange={e=>setAdminRule({...adminRule,course_id:Number(e.target.value)})}/>
            <input placeholder="Loại (prereq/coreq)" value={adminRule.rule_type} onChange={e=>setAdminRule({...adminRule,rule_type:e.target.value})}/>
            <input placeholder='{"course_codes":["CS101"]}' value={adminRule.rule_data} onChange={e=>setAdminRule({...adminRule,rule_data:e.target.value})}/>
          </FormCard>
        </div>
      )}

      {tab === "lists" && (
        <div>
          <button className="btn btn-outline" disabled={!token} onClick={onRefreshLists} style={{marginBottom:16}}>Tải lại dữ liệu</button>
          <div className="admin-lists-grid">
            <div className="card">
              <div className="card-header"><span className="card-title">Quy tắc ({rules.length})</span></div>
              <div className="card-body">
                {rules.length===0?<div className="empty-state-inline">Chưa có quy tắc</div>:(
                  <ul className="admin-list">{rules.map(r=>(
                    <li key={r.id}><span>#{r.id} {r.rule_type} | course={r.course_id??"tất cả"}</span>
                    <button className="btn btn-ghost btn-sm" onClick={()=>onAdminCreate(`/admin/rules/${r.id}`,{},"delete")}>Xóa</button></li>
                  ))}</ul>
                )}
              </div>
            </div>
            <div className="card">
              <div className="card-header"><span className="card-title">Đăng ký ({adminEnrollments.length})</span></div>
              <div className="card-body">
                {adminEnrollments.length===0?<div className="empty-state-inline">Chưa có</div>:(
                  <ul className="admin-list">{adminEnrollments.map(e=>(
                    <li key={e.id}><span>#{e.id} SV={e.student_id} HP={e.section_id} [{e.status}]</span>
                    <button className="btn btn-ghost btn-sm" onClick={()=>onAdminCreate(`/admin/enrollments/${e.id}/complete`,{})}>Hoàn thành</button></li>
                  ))}</ul>
                )}
              </div>
            </div>
            <div className="card">
              <div className="card-header"><span className="card-title">Sinh viên ({students.length})</span></div>
              <div className="card-body">
                {students.length===0?<div className="empty-state-inline">Chưa có</div>:(
                  <ul className="admin-list">{students.map(s=>(
                    <li key={s.id}>#{s.id} {s.student_number} | {s.major||"—"} | GPA: {s.gpa}</li>
                  ))}</ul>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === "reports" && (
        <div>
          <div className="filter-row" style={{marginBottom:16}}>
            <select value={reportTerm} onChange={e=>setReportTerm(e.target.value)}><option value="">Tất cả HK</option>{terms.map(t=><option key={t.id} value={t.id}>{t.name}</option>)}</select>
            <select value={reportCourse} onChange={e=>setReportCourse(e.target.value)}><option value="">Tất cả môn</option>{courses.map(c=><option key={c.id} value={c.id}>{c.code}</option>)}</select>
            <button className="btn btn-primary" disabled={!token} onClick={onFetchReports}>Tải báo cáo</button>
          </div>
          {reports.length===0?<div className="empty-state-inline">Chưa có dữ liệu</div>:(
            <div className="card"><div className="card-body">
              <table className="data-table"><thead><tr><th>Section</th><th>Đã ĐK</th><th>Sức chứa</th><th>Chờ</th><th>Tỉ lệ</th></tr></thead>
              <tbody>{reports.map(r=>(
                <tr key={r.section_id}><td>Section {r.section_id}</td><td>{r.enrolled}</td><td>{r.capacity}</td><td>{r.waitlisted}</td>
                <td><div className="progress-bar"><div className="progress-fill" style={{width:`${Math.min(100,r.utilization)}%`}}/></div><span className="progress-text">{r.utilization}%</span></td></tr>
              ))}</tbody></table>
            </div></div>
          )}
        </div>
      )}

      {tab === "import" && (
        <div className="card">
          <div className="card-header">
            <span className="card-title">Nhập dữ liệu CSV</span>
            <div style={{display:"flex",gap:8}}>
              <select value={csvTarget} onChange={e=>setCsvTarget(e.target.value)}>
                <option value="departments">Departments</option><option value="courses">Courses</option>
                <option value="terms">Terms</option><option value="sections">Sections</option>
              </select>
              <button className="btn btn-primary btn-sm" disabled={!token} onClick={()=>onAdminCreate(`/admin/import/${csvTarget}`,{csv:csvText})}>Import</button>
            </div>
          </div>
          <div className="card-body">
            <textarea className="csv-input" rows={10} placeholder="Dán CSV tại đây..." value={csvText} onChange={e=>setCsvText(e.target.value)}/>
          </div>
        </div>
      )}

      {tab === "instructor" && (
        <div className="card">
          <div className="card-header">
            <span className="card-title">Danh sách lớp</span>
            <div style={{display:"flex",gap:8,alignItems:"center"}}>
              <input placeholder="Section ID" value={instructorSectionId} onChange={e=>setInstructorSectionId(e.target.value)} style={{width:120}}/>
              <button className="btn btn-primary btn-sm" disabled={!token} onClick={onFetchRoster}>Tải</button>
              <button className="btn btn-outline btn-sm" onClick={()=>window.open(`http://localhost:8000/instructor/sections/${instructorSectionId}/roster.csv`,"_blank")}>CSV</button>
            </div>
          </div>
          <div className="card-body">
            {roster.length===0?<div className="empty-state-inline">Chọn section để xem</div>:(
              <table className="data-table"><thead><tr><th>MSSV</th><th>Ngành</th><th>GPA</th><th>Mã môn</th></tr></thead>
              <tbody>{roster.map(r=>(
                <tr key={r.enrollment_id}><td>{r.student_number}</td><td>{r.major||"—"}</td><td>{r.gpa}</td><td>{r.course_code}</td></tr>
              ))}</tbody></table>
            )}
          </div>
        </div>
      )}

      {tab === "notifications" && (
        <div className="card">
          <div className="card-header">
            <span className="card-title">Thông báo</span>
            <button className="btn btn-primary btn-sm" disabled={!token} onClick={onFetchNotifications}>Tải</button>
          </div>
          <div className="card-body">
            {notifications.length===0?<div className="empty-state-inline">Không có thông báo</div>:(
              <ul className="admin-list">{notifications.map(n=>(
                <li key={n.id}><span className={n.read?"read":"unread"}>{n.read?"✓":"●"} {n.title} — {n.body}</span></li>
              ))}</ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function FormCard({ title, children, disabled, onSubmit }) {
  return (
    <div className="card">
      <div className="card-header"><span className="card-title">{title}</span></div>
      <div className="card-body admin-form">
        {children}
        <button className="btn btn-primary" disabled={disabled} onClick={onSubmit}>Tạo {title}</button>
      </div>
    </div>
  );
}
