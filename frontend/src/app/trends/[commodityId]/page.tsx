type TrendPageProps = {
  params: { commodityId: string };
};

export default function TrendPage({ params }: TrendPageProps) {
  return (
    <section>
      <h1>Price Trends: {params.commodityId}</h1>
      <p>6-month trend chart will be added in the charts module.</p>
    </section>
  );
}
