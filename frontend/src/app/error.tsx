"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <section className="page">
      <div className="page-header">
        <h1>Something went wrong</h1>
        <p className="subtitle">{error.message || "Unexpected error while loading this page."}</p>
      </div>
      <div className="card" style={{ maxWidth: 400 }}>
        <button className="btn" type="button" onClick={reset}>
          Try again
        </button>
      </div>
    </section>
  );
}
