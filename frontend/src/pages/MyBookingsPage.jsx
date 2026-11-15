import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { formatDate } from "../utils";

export default function MyBookingsPage() {
  const [bookings, setBookings] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState(null);

  useEffect(() => {
    api
      .getMyBookings()
      .then(setBookings)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleCancel(booking) {
    const ok = window.confirm(
      `Odwołać rezerwację ${booking.origin} → ${booking.destination} (miejsca: ${booking.seats})?`
    );
    if (!ok) return;

    setError("");
    setCancellingId(booking.id);
    try {
      await api.cancelBooking(booking.id);
      setBookings((list) => list.filter((b) => b.id !== booking.id));
    } catch (err) {
      setError(err.message);
    } finally {
      setCancellingId(null);
    }
  }

  if (loading) return <main><p className="muted">Ładowanie…</p></main>;

  return (
    <main>
      <h1>Moje rezerwacje</h1>
      {error && <p className="error">{error}</p>}

      {bookings.length === 0 ? (
        <p className="muted">
          Nie masz jeszcze rezerwacji. <Link to="/">Przeglądaj przejazdy</Link>
        </p>
      ) : (
        bookings.map((b) => (
          <div key={b.id} className="card booking">
            <div>
              <Link to={`/rides/${b.ride_id}`} className="ride-route">
                {b.origin} → {b.destination}
              </Link>
              <p className="ride-meta">Odjazd: {formatDate(b.departure)}</p>
              <p className="ride-meta">
                Miejsca: <strong>{b.seats}</strong> · Razem:{" "}
                <strong>{(b.seats * b.price).toFixed(2)} zł</strong> · Kierowca: {b.driver_name}
              </p>
            </div>
            <button
              className="btn btn-danger"
              disabled={cancellingId === b.id}
              onClick={() => handleCancel(b)}
            >
              {cancellingId === b.id ? "Odwoływanie…" : "Odwołaj"}
            </button>
          </div>
        ))
      )}
    </main>
  );
}
