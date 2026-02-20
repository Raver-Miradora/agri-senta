"use client";

import { useEffect, useState, useCallback } from "react";
import {
  Wheat,
  Sprout,
  BarChart3,
  Plus,
  Trash2,
  Loader2,
  Calendar,
} from "lucide-react";
import {
  HarvestItem,
  HarvestSummary,
  Commodity,
  Region,
  fetchFromApi,
  fetchWithAuth,
} from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import SimpleBarChart from "@/components/charts/SimpleBarChart";

export default function HarvestsPage() {
  const { user } = useAuth();
  const isAdmin = user?.is_admin ?? false;

  const [harvests, setHarvests] = useState<HarvestItem[]>([]);
  const [summaries, setSummaries] = useState<HarvestSummary[]>([]);
  const [commodities, setCommodities] = useState<Commodity[]>([]);
  const [regions, setRegions] = useState<Region[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  /* Filters */
  const [season, setSeason] = useState("");
  const [commodityId, setCommodityId] = useState("");

  /* Add form */
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    region_id: "",
    commodity_id: "",
    quantity_kg: "",
    area_hectares: "",
    season: "",
    harvest_date: new Date().toISOString().slice(0, 10),
    farmer_name: "",
    notes: "",
  });
  const [submitting, setSubmitting] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams();
      if (season) params.set("season", season);
      if (commodityId) params.set("commodity_id", commodityId);
      const qs = params.toString();

      const [h, s, c, r] = await Promise.all([
        fetchFromApi<HarvestItem[]>(`/harvests${qs ? `?${qs}` : ""}`),
        fetchFromApi<HarvestSummary[]>(`/harvests/summary${qs ? `?${qs}` : ""}`),
        fetchFromApi<Commodity[]>("/commodities"),
        fetchFromApi<Region[]>("/regions"),
      ]);
      setHarvests(h);
      setSummaries(s);
      setCommodities(c);
      setRegions(r);
    } catch {
      setError("Failed to load harvest data");
    } finally {
      setLoading(false);
    }
  }, [season, commodityId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await fetchWithAuth("/harvests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          region_id: Number(formData.region_id),
          commodity_id: Number(formData.commodity_id),
          quantity_kg: Number(formData.quantity_kg),
          area_hectares: formData.area_hectares ? Number(formData.area_hectares) : null,
          season: formData.season || null,
          harvest_date: formData.harvest_date,
          farmer_name: formData.farmer_name || null,
          notes: formData.notes || null,
        }),
      });
      setShowForm(false);
      setFormData({
        region_id: "",
        commodity_id: "",
        quantity_kg: "",
        area_hectares: "",
        season: "",
        harvest_date: new Date().toISOString().slice(0, 10),
        farmer_name: "",
        notes: "",
      });
      loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add harvest record");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this harvest record?")) return;
    try {
      await fetchWithAuth(`/harvests/${id}`, { method: "DELETE" });
      loadData();
    } catch {
      setError("Failed to delete record");
    }
  };

  const totalKg = summaries.reduce((s, r) => s + r.total_kg, 0);
  const chartData = summaries.slice(0, 12).map((s) => ({
    commodity: s.commodity_name.length > 12 ? s.commodity_name.slice(0, 12) + "…" : s.commodity_name,
    total_kg: s.total_kg,
  }));

  return (
    <section className="page">
      <div className="page-header">
        <div className="page-header-row">
          <div className="page-icon page-icon-green">
            <Wheat size={22} />
          </div>
          <div>
            <h1>Harvest Tracking</h1>
            <p className="subtitle">
              Seasonal crop harvest records across Lagonoy barangays.
              Track yields, monitor productivity, and plan agricultural programs.
            </p>
          </div>
        </div>
      </div>

      {/* KPI row */}
      <div className="grid-4">
        <div className="card kpi kpi-accent-green">
          <div className="kpi-top">
            <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Total Yield</span>
            <div className="kpi-icon kpi-icon-green"><Sprout size={20} /></div>
          </div>
          <p className="kpi-value">{(totalKg / 1000).toFixed(1)} MT</p>
          <p className="kpi-label">{summaries.length} commodities recorded</p>
        </div>
        <div className="card kpi kpi-accent-blue">
          <div className="kpi-top">
            <span style={{ fontSize: "0.82rem", color: "var(--muted)" }}>Records</span>
            <div className="kpi-icon kpi-icon-blue"><Calendar size={20} /></div>
          </div>
          <p className="kpi-value">{harvests.length}</p>
          <p className="kpi-label">harvest entries</p>
        </div>
      </div>

      {/* Filters */}
      <div className="card" style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem", alignItems: "center", padding: "0.75rem 1.25rem" }}>
        <select className="filter-select" value={season} onChange={(e) => setSeason(e.target.value)}>
          <option value="">All Seasons</option>
          <option value="Dry">Dry Season</option>
          <option value="Wet">Wet Season</option>
          <option value="Year-Round">Year-Round</option>
        </select>
        <select className="filter-select" value={commodityId} onChange={(e) => setCommodityId(e.target.value)}>
          <option value="">All Commodities</option>
          {commodities.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
        {isAdmin && (
          <button className="btn btn-primary" style={{ marginLeft: "auto" }} onClick={() => setShowForm(!showForm)}>
            <Plus size={16} /> Add Record
          </button>
        )}
      </div>

      {error && <p style={{ color: "var(--agri-red)", fontWeight: 600 }}>{error}</p>}

      {/* Add form */}
      {showForm && isAdmin && (
        <div className="card">
          <div className="card-header">
            <div className="card-header-icon page-icon-green"><Sprout size={18} /></div>
            <h3 className="section-title">New Harvest Record</h3>
          </div>
          <form onSubmit={handleSubmit} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
            <select required className="filter-select" value={formData.region_id} onChange={(e) => setFormData({ ...formData, region_id: e.target.value })}>
              <option value="">Select Barangay</option>
              {regions.map((r) => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>
            <select required className="filter-select" value={formData.commodity_id} onChange={(e) => setFormData({ ...formData, commodity_id: e.target.value })}>
              <option value="">Select Commodity</option>
              {commodities.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
            <input required type="number" step="0.01" placeholder="Quantity (kg)" className="filter-select" value={formData.quantity_kg} onChange={(e) => setFormData({ ...formData, quantity_kg: e.target.value })} />
            <input type="number" step="0.01" placeholder="Area (hectares)" className="filter-select" value={formData.area_hectares} onChange={(e) => setFormData({ ...formData, area_hectares: e.target.value })} />
            <select className="filter-select" value={formData.season} onChange={(e) => setFormData({ ...formData, season: e.target.value })}>
              <option value="">Season (optional)</option>
              <option value="Dry">Dry</option>
              <option value="Wet">Wet</option>
              <option value="Year-Round">Year-Round</option>
            </select>
            <input required type="date" className="filter-select" value={formData.harvest_date} onChange={(e) => setFormData({ ...formData, harvest_date: e.target.value })} />
            <input type="text" placeholder="Farmer name (optional)" className="filter-select" value={formData.farmer_name} onChange={(e) => setFormData({ ...formData, farmer_name: e.target.value })} />
            <input type="text" placeholder="Notes (optional)" className="filter-select" value={formData.notes} onChange={(e) => setFormData({ ...formData, notes: e.target.value })} />
            <div style={{ gridColumn: "1 / -1", display: "flex", gap: "0.5rem", justifyContent: "flex-end" }}>
              <button type="button" className="btn btn-outline" onClick={() => setShowForm(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? <><Loader2 size={16} className="spin" /> Saving…</> : "Save Record"}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Chart */}
      {chartData.length > 0 && (
        <div className="card">
          <div className="card-header">
            <div className="card-header-icon page-icon-green"><BarChart3 size={18} /></div>
            <h3 className="section-title">Top Commodities by Volume</h3>
          </div>
          <div className="chart-container">
            <SimpleBarChart data={chartData} xKey="commodity" yKey="total_kg" />
          </div>
        </div>
      )}

      {/* Records table */}
      <div className="card">
        <div className="card-header">
          <div className="card-header-icon page-icon-blue"><Wheat size={18} /></div>
          <div>
            <h3 className="section-title">Harvest Records</h3>
            <p className="section-subtitle">{harvests.length} entries</p>
          </div>
        </div>
        {loading ? (
          <p style={{ textAlign: "center", color: "var(--muted)", padding: "2rem 0" }}>Loading…</p>
        ) : harvests.length === 0 ? (
          <div className="empty">
            <div className="empty-icon"><Wheat size={24} /></div>
            <p>No harvest records found. {isAdmin ? "Click 'Add Record' to log a harvest." : ""}</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Commodity</th>
                  <th>Barangay</th>
                  <th style={{ textAlign: "right" }}>Quantity&nbsp;(kg)</th>
                  <th>Season</th>
                  <th>Farmer</th>
                  {isAdmin && <th />}
                </tr>
              </thead>
              <tbody>
                {harvests.map((h) => (
                  <tr key={h.id}>
                    <td style={{ whiteSpace: "nowrap" }}>{h.harvest_date}</td>
                    <td style={{ fontWeight: 600 }}>{h.commodity_name}</td>
                    <td>{h.region_name}</td>
                    <td style={{ textAlign: "right", fontWeight: 600 }}>
                      {h.quantity_kg.toLocaleString("en-PH", { maximumFractionDigits: 1 })}
                    </td>
                    <td>{h.season ?? "—"}</td>
                    <td>{h.farmer_name ?? "—"}</td>
                    {isAdmin && (
                      <td>
                        <button className="btn-icon" title="Delete" onClick={() => handleDelete(h.id)}>
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
