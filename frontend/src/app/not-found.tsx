import Link from "next/link";

export default function NotFound() {
  return (
    <section className="page">
      <div className="page-header">
        <h1>Page not found</h1>
        <p className="subtitle">The page you requested does not exist.</p>
      </div>
      <div className="card" style={{ maxWidth: 400 }}>
        <Link className="btn" href="/">
          Go back to dashboard
        </Link>
      </div>
    </section>
  );
}
