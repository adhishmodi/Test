const vehicleClasses = ["Cars", "Motorcycles", "Buses", "Trucks"];

export default function App() {
  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">COMPUTER VISION · TRAFFIC ANALYTICS</p>
          <h1>Intelligent Traffic Monitoring</h1>
        </div>
        <span className="status-pill">Development preview</span>
      </header>

      <section className="welcome-panel" aria-labelledby="welcome-title">
        <p className="eyebrow">TRAFFIC INSIGHTS</p>
        <h2 id="welcome-title">Your monitoring workspace</h2>
        <p>
          Analyze urban-road images and videos to explore vehicle detection, tracking,
          traffic density and congestion.
        </p>
        <p className="notice">
          Analysis workflows are not connected yet. This screen is the initial UI scaffold.
        </p>
      </section>

      <section className="class-grid" aria-label="Supported vehicle categories">
        {vehicleClasses.map((vehicleClass) => (
          <article className="class-card" key={vehicleClass}>
            <span className="class-label">{vehicleClass}</span>
            <strong>—</strong>
            <span className="muted">Awaiting analysis</span>
          </article>
        ))}
      </section>

      <footer>
        Educational prototype · Results and performance metrics will appear after analysis is
        implemented.
      </footer>
    </main>
  );
}
