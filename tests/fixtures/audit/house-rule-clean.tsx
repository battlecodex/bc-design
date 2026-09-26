export function Plan() {
  return (
    <div className="fixed inset-0 bg-[var(--bc-scrim)]">
      <section role="dialog" aria-labelledby="plan-title">
        <p className="text-sm font-medium text-muted-foreground">New plan</p>
        <h2 id="plan-title">Weekly review</h2>
        <p>Synced with your calendar</p>
        <button className="rounded-md bg-neutral-900 px-4 py-2 text-white focus-visible:ring-2 focus-visible:ring-[var(--bc-accent-strong)]">
          Save plan
        </button>
      </section>
    </div>
  );
}
