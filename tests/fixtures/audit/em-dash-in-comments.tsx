/**
 * Task list — renders one row per task.
 */
export function TaskList({ count }: { count: number }) {
  // Loading state — keep the skeleton height stable.
  const load = () => {
    /* retry — once */
    return fetch("https://example.com/api/tasks");
  };
  return (
    <section className="p-4">
      {/* Header — title and count */}
      <h1>Your tasks</h1>
      <p>{count} due today</p>
    </section>
  );
}
