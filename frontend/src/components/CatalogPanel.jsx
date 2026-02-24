export default function CatalogPanel({
  courses, sections, terms, departments,
  selectedTerm, setSelectedTerm, selectedCourse, setSelectedCourse,
  enrollments, token, onEnroll, onDrop,
  cart, onAddToCart, onRemoveFromCart, onValidateCart, onEstimateBill, cartMessage,
  meetingTimes, authMessage
}) {
  function getScheduleByDay() {
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
    const items = {};
    days.forEach((d) => (items[d] = []));
    enrollments.forEach((e) => {
      const s = sections.find((sec) => sec.id === e.section_id);
      if (!s) return;
      const course = courses.find((c) => c.id === s.course_id);
      const mts = meetingTimes[s.id] || [];
      mts.forEach((mt) => {
        items[mt.day_of_week]?.push({
          label: course ? course.code : "Course",
          title: course ? course.title : "",
          time: `${mt.start_time} - ${mt.end_time}`,
          section: s.section_number,
          location: s.location,
        });
      });
    });
    return items;
  }

  const dayNames = { Mon: "Thứ 2", Tue: "Thứ 3", Wed: "Thứ 4", Thu: "Thứ 5", Fri: "Thứ 6" };
  const schedule = getScheduleByDay();

  return (
    <div className="catalog-panel">
      {/* Search / Filters */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            Tìm kiếm học phần
          </span>
        </div>
        <div className="card-body">
          <div className="filter-row">
            <select value={selectedTerm} onChange={(e) => setSelectedTerm(e.target.value)}>
              <option value="">Tất cả học kỳ</option>
              {terms.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
            <select value={selectedCourse} onChange={(e) => setSelectedCourse(e.target.value)}>
              <option value="">Tất cả môn học</option>
              {courses.map((c) => <option key={c.id} value={c.id}>{c.code} - {c.title}</option>)}
            </select>
          </div>
        </div>
      </div>

      {authMessage && <div className="toast-message">{authMessage}</div>}

      {/* Section Cards */}
      <div className="section-grid">
        {sections.map((s) => {
          const course = courses.find((c) => c.id === s.course_id);
          const enrolled = enrollments.some((e) => e.section_id === s.id);
          const inCart = cart.includes(s.id);
          const dept = departments.find(d => d.id === course?.department_id);
          return (
            <div key={s.id} className="card section-card">
              <div className="section-dept">{dept?.code || ""}</div>
              <div className="section-course">{course ? course.code : "—"}</div>
              <div className="section-title">{course ? course.title : "Section"}</div>
              <div className="section-meta">
                <div className="meta-item"><span className="meta-label">Nhóm</span><span>{s.section_number}</span></div>
                <div className="meta-item"><span className="meta-label">Sức chứa</span><span>{s.capacity}</span></div>
                <div className="meta-item"><span className="meta-label">Hình thức</span><span>{s.delivery_mode}</span></div>
                <div className="meta-item"><span className="meta-label">Phòng</span><span>{s.location || "TBA"}</span></div>
                <div className="meta-item"><span className="meta-label">Tín chỉ</span><span>{course?.credits_max || "—"}</span></div>
              </div>
              <div className="section-badges">
                <span className={`badge ${s.status === "open" ? "badge-success" : "badge-muted"}`}>{s.status === "open" ? "Mở" : s.status}</span>
                {enrolled && <span className="badge badge-primary">Đã đăng ký</span>}
              </div>
              <div className="section-actions">
                <button className="btn btn-primary btn-sm" disabled={!token || enrolled} onClick={() => onEnroll(s.id)}>
                  {enrolled ? "✓ Đã ĐK" : "Đăng ký"}
                </button>
                <button className="btn btn-outline btn-sm" disabled={!token || inCart} onClick={() => onAddToCart(s.id)}>
                  {inCart ? "Trong giỏ" : "+ Giỏ"}
                </button>
                {enrolled && (
                  <button className="btn btn-danger btn-sm" onClick={() => onDrop(s.id)}>Hủy</button>
                )}
              </div>
            </div>
          );
        })}
        {sections.length === 0 && (
          <div className="card" style={{ gridColumn: "1 / -1", textAlign: "center", padding: 40 }}>
            <div className="empty-state-inline">Không tìm thấy học phần nào</div>
          </div>
        )}
      </div>

      {/* Schedule View */}
      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-header">
          <span className="card-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
            Thời khóa biểu
          </span>
        </div>
        <div className="card-body">
          {enrollments.length === 0 ? (
            <div className="empty-state-inline">Chưa đăng ký học phần nào</div>
          ) : (
            <div className="schedule-grid">
              {Object.entries(schedule).map(([day, items]) => (
                <div key={day} className="schedule-col">
                  <div className="schedule-day-name">{dayNames[day] || day}</div>
                  {items.length === 0 && <div className="schedule-empty">—</div>}
                  {items.map((item, idx) => (
                    <div key={idx} className="schedule-block">
                      <div className="schedule-block-course">{item.label}</div>
                      <div className="schedule-block-title">{item.title}</div>
                      <div className="schedule-block-time">{item.time}</div>
                      <div className="schedule-block-loc">{item.location}</div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Cart */}
      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-header">
          <span className="card-title">
            🛒 Giỏ đăng ký ({cart.length})
          </span>
          <div style={{ display: "flex", gap: 8 }}>
            <button className="btn btn-primary btn-sm" disabled={!token || cart.length === 0} onClick={onValidateCart}>Kiểm tra</button>
            <button className="btn btn-outline btn-sm" disabled={!token || cart.length === 0} onClick={onEstimateBill}>Ước tính phí</button>
          </div>
        </div>
        <div className="card-body">
          {cartMessage && <div className="cart-message">{cartMessage}</div>}
          {cart.length === 0 ? (
            <div className="empty-state-inline">Giỏ đăng ký trống</div>
          ) : (
            <div className="cart-list">
              {cart.map((id) => {
                const s = sections.find((sec) => sec.id === id);
                const c = courses.find((co) => co.id === s?.course_id);
                return (
                  <div key={id} className="cart-item">
                    <div className="cart-item-info">
                      <span className="cart-item-code">{c ? c.code : "—"}</span>
                      <span className="cart-item-name">{c ? c.title : "Section"}</span>
                      <span className="cart-item-sec">Nhóm {s?.section_number}</span>
                    </div>
                    <div className="cart-item-actions">
                      <button className="btn btn-primary btn-sm" onClick={() => onEnroll(id)}>Đăng ký</button>
                      <button className="btn btn-ghost btn-sm" onClick={() => onRemoveFromCart(id)}>Xóa</button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
