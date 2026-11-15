import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { useAuth } from "../auth/AuthContext";
import { formatDate } from "../utils";

export default function RidesPage() {
  const { user } = useAuth();
  const [rides, setRides] = useState([]);
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false; 
    api
      .getRides({ origin, destination })
      .then((data) => {
        if (!cancelled) {
          setRides(data);
          setError("");
        }
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [origin, destination]);

  return (
    <main>
      <h1>Dostępne przejazdy</h1>

      {!user && (
        <p className="notice">
          Przeglądasz jako gość. <Link to="/login">Zaloguj się</Link>, aby zobaczyć szczegóły
          i zarezerwować miejsce.
        </p>
      )}

      <div className="filters">
        <input placeholder="Skąd" value={origin} onChange={(e) => setOrigin(e.target.value)} />
        <input placeholder="Dokąd" value={destination} onChange={(e) => setDestination(e.target.value)} />
      </div>

      {error && <p className="error">{error}</p>}
      {loading && <p className="muted">Ładowanie…</p>}
      {!loading && !error && rides.length === 0 && (
        <p className="muted">Brak przejazdów dla podanych kryteriów.</p>
      )}

      {rides.map((ride) => (
        <Link key={ride.id} to={`/rides/${ride.id}`} className="ride-card">
          <div className="ride-route">
            {ride.origin} → {ride.destination}
          </div>
          <div className="ride-meta">
            {formatDate(ride.departure)} · wolne miejsca: {ride.seats_left} · {ride.price} zł
          </div>
          <div className="muted">Kierowca: {ride.driver_name}</div>
        </Link>
      ))}
    </main>
  );
}
