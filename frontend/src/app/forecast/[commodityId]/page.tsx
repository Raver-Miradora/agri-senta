type ForecastCommodityPageProps = {
  params: { commodityId: string };
};

export default function ForecastCommodityPage({ params }: ForecastCommodityPageProps) {
  return (
    <section>
      <h1>Forecast Detail: {params.commodityId}</h1>
      <p>Commodity-level forecast chart will be added in the forecast module.</p>
    </section>
  );
}
