export function Card() {
  return (
    <>
      <div className="rounded-md border transition-colors duration-150 ease-[var(--bc-ease)]">Weekly report</div>
      <aside className="drawer translate-x-0 transition-transform duration-[400ms] ease-[var(--bc-ease)]">Filters</aside>
      <h1 className="reveal opacity-100 transition-opacity duration-[600ms] ease-[var(--bc-ease)]">Plan the week</h1>
    </>
  );
}
