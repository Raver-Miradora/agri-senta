export default function Loading() {
  return (
    <section className="page">
      <div className="page-header">
        <h1>Loading…</h1>
        <p className="subtitle">Please wait while Agri-Senta prepares your dashboard.</p>
      </div>
      <div className="grid">
        <div className="card skeleton" style={{ height: 100 }} />
        <div className="card skeleton" style={{ height: 100 }} />
        <div className="card skeleton" style={{ height: 100 }} />
      </div>
    </section>
  );
}
