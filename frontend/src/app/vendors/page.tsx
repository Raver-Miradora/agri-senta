"use client";

import { useEffect, useState, useCallback } from "react";
import {
  Store,
  Plus,
  Trash2,
  Loader2,
  Phone,
  MapPin,
  Search,
} from "lucide-react";
import {
  VendorItem,
  Market,
  fetchFromApi,
  fetchWithAuth,
} from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";

export default function VendorsPage() {
  const { user } = useAuth();
  const isAdmin = user?.is_admin ?? false;

  const [vendors, setVendors] = useState<VendorItem[]>([]);
  const [markets, setMarkets] = useState<Market[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  /* Filters */
  const [marketFilter, setMarketFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  /* Add form */
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    stall_number: "",
    market_id: "",
    commodity_type: "",
    contact_number: "",
  });
  const [submitting, setSubmitting] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams();
      if (marketFilter) params.set("market_id", marketFilter);
      if (typeFilter) params.set("commodity_type", typeFilter);
      const qs = params.toString();

      const [v, m] = await Promise.all([
        fetchFromApi<VendorItem[]>(`/vendors${qs ? `?${qs}` : ""}`),
        fetchFromApi<Market[]>("/markets"),
      ]);
      setVendors(v);
      setMarkets(m);
    } catch {
      setError("Failed to load vendor data");
    } finally {
      setLoading(false);
    }
  }, [marketFilter, typeFilter]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await fetchWithAuth("/vendors", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: formData.name,
          stall_number: formData.stall_number || null,
          market_id: formData.market_id ? Number(formData.market_id) : null,
          commodity_type: formData.commodity_type || null,
          contact_number: formData.contact_number || null,
        }),
      });
      setShowForm(false);
      setFormData({ name: "", stall_number: "", market_id: "", commodity_type: "", contact_number: "" });
      loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add vendor");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Remove this vendor?")) return;
    try {
      await fetchWithAuth(`/vendors/${id}`, { method: "DELETE" });
      loadData();
    } catch {
      setError("Failed to remove vendor");
    }
  };

  const commodityTypes = Array.from(new Set(vendors.map((v) => v.commodity_type).filter(Boolean))) as string[];

  const filtered = vendors.filter((v) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return v.name.toLowerCase().includes(q) || (v.stall_number?.toLowerCase().includes(q));
  });

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-yellow">
            <Store size={22} />
          </div>
          <div>
            <h1>Vendor Directory</h1>
            <p className="subtitle">
              Registered market vendors across Lagonoy public markets.
              Filter by market or commodity type.
            </p>
          </div>
        </div>
      </div>

      {/* KPI */}
      <div className="grid-4">
        <div className="card kpi kpi-accent-yellow">
          <div className="kpi-top">
            <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Active Vendors</span>
            <div className="kpi-icon kpi-icon-yellow"><Store size={20} /></div>
          </div>
          <p className="kpi-value">{vendors.filter((v) => v.is_active).length}</p>
          <p className="kpi-label">of {vendors.length} total vendors</p>
        </div>
        <div className="card kpi kpi-accent-blue">
          <div className="kpi-top">
            <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Markets</span>
            <div className="kpi-icon kpi-icon-blue"><MapPin size={20} /></div>
          </div>
          <p className="kpi-value">{markets.length}</p>
          <p className="kpi-label">Lagonoy market locations</p>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem", alignItems: "center", padding: "0.75rem 1.25rem" }}>
        <div className="search-wrap" style={{ flex: "1 1 200px", maxWidth: 320 }}>
          <Search size={16} className="search-icon" />
          <input
            className="search-input"
            placeholder="Search vendors…"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <select className="filter-select" value={marketFilter} onChange={(e) => setMarketFilter(e.target.value)}>
          <option value="">All Markets</option>
          {markets.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
        </select>
        <select className="filter-select" value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
          <option value="">All Types</option>
          {commodityTypes.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        {isAdmin && (
          <button className="btn btn-primary" style={{ marginLeft: "auto" }} onClick={() => setShowForm(!showForm)}>
            <Plus size={16} /> Add Vendor
          </button>
        )}
      </div>

      {error && <p style={{ color: "var(--agri-red)", fontWeight: 600 }}>{error}</p>}

      {/* Add form */}
      {showForm && isAdmin && (
        <div className="card">
          <div className="card-header">
            <div className="card-header-icon page-icon-yellow"><Store size={18} /></div>
            <h3 className="section-title">Register New Vendor</h3>
          </div>
          <form onSubmit={handleSubmit} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
            <input required type="text" placeholder="Vendor Name *" className="filter-select" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
            <input type="text" placeholder="Stall Number" className="filter-select" value={formData.stall_number} onChange={(e) => setFormData({ ...formData, stall_number: e.target.value })} />
            <select className="filter-select" value={formData.market_id} onChange={(e) => setFormData({ ...formData, market_id: e.target.value })}>
              <option value="">Select Market</option>
              {markets.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
            </select>
            <input type="text" placeholder="Commodity Type (e.g. Vegetables)" className="filter-select" value={formData.commodity_type} onChange={(e) => setFormData({ ...formData, commodity_type: e.target.value })} />
            <input type="text" placeholder="Contact Number" className="filter-select" value={formData.contact_number} onChange={(e) => setFormData({ ...formData, contact_number: e.target.value })} />
            <div style={{ display: "flex", gap: "0.5rem", justifyContent: "flex-end", alignItems: "center" }}>
              <button type="button" className="btn btn-outline" onClick={() => setShowForm(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? <><Loader2 size={16} className="spin" /> Saving…</> : "Register"}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Vendor cards */}
      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-yellow"><Store size={18} /></div>
          <div>
            <h3 className="section-title">Vendor List</h3>
            <p className="section-subtitle">{filtered.length} vendor{filtered.length !== 1 ? "s" : ""}</p>
          </div>
        </div>
        {loading ? (
          <p style={{ textAlign: "center", color: "var(--muted)", padding: "2rem 0" }}>Loading…</p>
        ) : filtered.length === 0 ? (
          <div className="empty">
            <div className="empty-icon"><Store size={24} /></div>
            <p>No vendors found. {isAdmin ? "Click 'Add Vendor' to register one." : ""}</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Stall</th>
                  <th>Market</th>
                  <th>Type</th>
                  <th>Contact</th>
                  <th>Status</th>
                  {isAdmin && <th />}
                </tr>
              </thead>
              <tbody>
                {filtered.map((v) => (
                  <tr key={v.id}>
                    <td style={{ fontWeight: 600 }}>{v.name}</td>
                    <td>{v.stall_number ?? "—"}</td>
                    <td>{v.market_name ?? "—"}</td>
                    <td>{v.commodity_type ?? "—"}</td>
                    <td>
                      {v.contact_number ? (
                        <span style={{ display: "inline-flex", alignItems: "center", gap: "0.25rem" }}>
                          <Phone size={12} /> {v.contact_number}
                        </span>
                      ) : "—"}
                    </td>
                    <td>
                      <span className={`badge ${v.is_active ? "badge-green" : "badge-red"}`}>
                        {v.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                    {isAdmin && (
                      <td>
                        <button className="btn-icon" title="Remove" onClick={() => handleDelete(v.id)}>
                          <Trash2 size={14} />
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}
