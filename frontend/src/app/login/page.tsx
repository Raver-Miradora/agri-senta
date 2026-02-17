"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { LogIn } from "lucide-react";
import { useAuth } from "@/lib/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const { login, user } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // If already logged in, redirect
  if (user) {
    router.replace(user.is_admin ? "/admin" : "/");
    return null;
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      router.push("/admin");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="section">
      <div style={{ maxWidth: 400, margin: "0 auto" }}>
        <div className="card" style={{ padding: "2rem" }}>
          <h1
            className="section-title"
            style={{ display: "flex", alignItems: "center", gap: 8 }}
          >
            <LogIn size={24} />
            Admin Login
          </h1>
          <p style={{ color: "var(--text-secondary)", marginBottom: "1.5rem" }}>
            Sign in to access the admin dashboard.
          </p>

          {error && (
            <div
              style={{
                background: "var(--agri-red-light, #fee2e2)",
                color: "var(--agri-red, #dc2626)",
                padding: "0.75rem 1rem",
                borderRadius: 8,
                marginBottom: "1rem",
                fontSize: "0.875rem",
              }}
            >
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: "1rem" }}>
              <label
                htmlFor="username"
                style={{
                  display: "block",
                  marginBottom: 4,
                  fontWeight: 500,
                  fontSize: "0.875rem",
                }}
              >
                Username
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoComplete="username"
                style={{
                  width: "100%",
                  padding: "0.625rem 0.75rem",
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                  fontSize: "0.9375rem",
                  outline: "none",
                  boxSizing: "border-box",
                }}
              />
            </div>

            <div style={{ marginBottom: "1.5rem" }}>
              <label
                htmlFor="password"
                style={{
                  display: "block",
                  marginBottom: 4,
                  fontWeight: 500,
                  fontSize: "0.875rem",
                }}
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                style={{
                  width: "100%",
                  padding: "0.625rem 0.75rem",
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                  fontSize: "0.9375rem",
                  outline: "none",
                  boxSizing: "border-box",
                }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
              style={{
                width: "100%",
                padding: "0.75rem",
                fontSize: "1rem",
                fontWeight: 600,
                borderRadius: 8,
                border: "none",
                cursor: loading ? "not-allowed" : "pointer",
                opacity: loading ? 0.7 : 1,
                background: "var(--agri-green)",
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: 8,
              }}
            >
              <LogIn size={18} />
              {loading ? "Signing in\u2026" : "Sign In"}
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}
