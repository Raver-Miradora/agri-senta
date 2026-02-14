import { Commodity, Region, fetchFromApi } from "@/lib/api";

export default async function HomePage() {
  const [commodities, regions] = await Promise.all([
    fetchFromApi<Commodity[]>("/commodities"),
    fetchFromApi<Region[]>("/regions"),
  ]);

  return (
    <section>
      <h1>Smart Palengke Dashboard</h1>
      <p>Live baseline data from the Agri-Senta API.</p>
      <div className="grid" style={{ marginTop: "1rem" }}>
        <div className="card">
          <h3>Tracked Commodities</h3>
          <p>{commodities.length}</p>
        </div>
        <div className="card">
          <h3>Tracked Regions</h3>
          <p>{regions.length}</p>
        </div>
      </div>
    </section>
  );
}
