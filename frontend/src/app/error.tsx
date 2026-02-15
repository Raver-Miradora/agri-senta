"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <section>
      <h1>Something went wrong</h1>
      <p>{error.message || "Unexpected error while loading this page."}</p>
      <button type="button" onClick={reset} style={{ marginTop: "0.75rem" }}>
        Try again
      </button>
    </section>
  );
}
