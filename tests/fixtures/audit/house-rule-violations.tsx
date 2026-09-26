export function Plan() {
  return (
    <div className="fixed inset-0 bg-black/60">
      <section role="dialog" aria-labelledby="plan-title">
        <p className="text-xs uppercase tracking-widest">New plan</p>
        <h2 id="plan-title">Weekly review</h2>
        <p>✓ Synced with your calendar</p>
        <button className="rounded-md bg-neutral-900 px-4 py-2 text-white">Save plan</button>
      </section>
    </div>
  );
}
