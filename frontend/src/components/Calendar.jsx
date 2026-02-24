import { useState } from "react";

const WEEKDAYS = ["CN", "T2", "T3", "T4", "T5", "T6", "T7"];

export default function Calendar() {
  const today = new Date();
  const [viewDate, setViewDate] = useState(new Date(today.getFullYear(), today.getMonth(), 1));
  const [selected, setSelected] = useState(today.getDate());

  const year = viewDate.getFullYear();
  const month = viewDate.getMonth();
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const cells = [];
  for (let i = 0; i < firstDay; i++) cells.push(null);
  for (let d = 1; d <= daysInMonth; d++) cells.push(d);

  const isToday = (d) =>
    d === today.getDate() && month === today.getMonth() && year === today.getFullYear();

  return (
    <div className="calendar">
      <div className="cal-nav">
        <button className="cal-arrow" onClick={() => setViewDate(new Date(year, month - 1, 1))}>‹</button>
        <span className="cal-month">tháng {month + 1} {year}</span>
        <button className="cal-arrow" onClick={() => setViewDate(new Date(year, month + 1, 1))}>›</button>
      </div>
      <div className="cal-grid">
        {WEEKDAYS.map((wd) => (
          <div key={wd} className="cal-wday">{wd}</div>
        ))}
        {cells.map((d, i) => (
          <div
            key={i}
            className={[
              "cal-cell",
              !d ? "empty" : "",
              d && isToday(d) ? "today" : "",
              d && d === selected && month === today.getMonth() && year === today.getFullYear() ? "selected" : "",
            ].filter(Boolean).join(" ")}
            onClick={() => d && setSelected(d)}
          >
            {d}
          </div>
        ))}
      </div>
    </div>
  );
}
