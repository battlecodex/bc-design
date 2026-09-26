const icons = { "✓": "check", "→": "next" };

export function Steps() {
  return (
    <ol>
      <li>Done ✓ → next ★</li>
      <li>Review the plan ↗</li>
      <li key="→">Plain words</li>
      <li>{/* Done ✓ → */}Only words</li>
      <li>Press <kbd>⌘↵</kbd> to send</li>
    </ol>
  );
}
