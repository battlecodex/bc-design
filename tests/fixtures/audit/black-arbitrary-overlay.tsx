export function Overlays() {
  return (
    <>
      <div className="fixed inset-0 bg-[#000]/50" />
      <div className="fixed inset-0 bg-[#000000]" />
      <div className="fixed inset-0 bg-[rgb(0_0_0/0.5)]" />
      <div className="fixed inset-0 bg-[rgba(0,0,0,0.4)]" />
      <div className="overlay" style={{ background: "#000" }} />
      <span className="rounded bg-[#000] px-2 text-white">Opaque label</span>
    </>
  );
}
