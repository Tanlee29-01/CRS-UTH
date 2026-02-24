export default function EmptyState({ icon = "📋", message = "Không có dữ liệu cho học kỳ này!" }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">{icon}</div>
      <p className="empty-text">{message}</p>
    </div>
  );
}
