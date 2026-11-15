import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import { useAuth } from "../auth/AuthContext";
import { formatDate } from "../utils";

export default function RideDetailPage() {
  const { id } = useParams(); 
  const { user } = useAuth();
  const [ride, setRide] = useState(null);
  const [seats, setSeats] = useState(1);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getRide(id)
      .then(setRide)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  async function handleBook(e) {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const updated = await api.bookRide(id, Number(seats));
      setRide(updated);
      setSeats(1);
      setSuccess(`Zarezerwowano miejsca: ${seats}. Dziękujemy!`);
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) return <main><p className="muted">Ładowanie…</p></main>;
  if (!ride) {
    return (
      <main>
        <p className="error">{error || "Nie znaleziono przejazdu"}</p>
        <Link to="/">← Wróć do listy</Link>
      </main>
    );
  }

  return (
    <main>
      <Link to="/">← Wróć do listy</Link>

      <div className="card">
        <h1>{ride.origin} → {ride.destination}</h1>
        <p>Odjazd: <strong>{formatDate(ride.departure)}</strong></p>
        <p>Cena za miejsce: <strong>{ride.price} zł</strong></p>
        <p>Wolne miejsca: <strong>{ride.seats_left}</strong></p>
        <p>Kierowca: <strong>{ride.driver_name}</strong></p>
      </div>

      {error && <p className="error">{error}</p>}
      {success && (
        <p className="success">
          {success} <Link to="/bookings">Zobacz moje rezerwacje</Link>
        </p>
      )}

      {user.is_driver ? (
        <p className="notice">Jesteś zalogowany jako kierowca, więc rezerwacja jest niedostępna.</p>
      ) : ride.seats_left === 0 ? (
        <p className="notice">Brak wolnych miejsc.</p>
      ) : (
        <form onSubmit={handleBook} className="form">
          <label>
            Liczba miejsc
            <input
              type="number"
              min="1"
              max={ride.seats_left}
              value={seats}
              onChange={(e) => setSeats(e.target.value)}
            />
          </label>
          <button type="submit" className="btn">Zarezerwuj</button>
        </form>
      )}
    </main>
  );
}
