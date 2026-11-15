import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

export default function AddRidePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    origin: "",
    destination: "",
    departure: "", 
    seats: 3,
    price: 50,
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  
  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (form.origin.trim().toLowerCase() === form.destination.trim().toLowerCase()) {
      return setError("Miejsce startu i celu muszą być różne");
    }
    if (new Date(form.departure) <= new Date()) {
      return setError("Data odjazdu musi być w przyszłości");
    }
    if (Number(form.seats) < 1) return setError("Liczba miejsc musi wynosić co najmniej 1");
    if (Number(form.price) < 0) return setError("Cena nie może być ujemna");

    setSubmitting(true);
    try {
      const ride = await api.createRide({
        origin: form.origin.trim(),
        destination: form.destination.trim(),
        departure: new Date(form.departure).toISOString(),
        seats: Number(form.seats),
        price: Number(form.price),
      });
      navigate(`/rides/${ride.id}`);
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  }

  return (
    <main className="narrow">
      <h1>Dodaj przejazd</h1>

      <form onSubmit={handleSubmit} className="form">
        <label>
          Skąd
          <input name="origin" value={form.origin} onChange={handleChange} required />
        </label>
        <label>
          Dokąd
          <input name="destination" value={form.destination} onChange={handleChange} required />
        </label>
        <label>
          Data i godzina odjazdu
          <input type="datetime-local" name="departure" value={form.departure} onChange={handleChange} required />
        </label>
        <label>
          Liczba wolnych miejsc
          <input type="number" min="1" max="8" name="seats" value={form.seats} onChange={handleChange} required />
        </label>
        <label>
          Cena za miejsce (zł)
          <input type="number" min="0" step="1" name="price" value={form.price} onChange={handleChange} required />
        </label>

        {error && <p className="error">{error}</p>}
        <button type="submit" className="btn" disabled={submitting}>
          {submitting ? "Zapisywanie…" : "Dodaj przejazd"}
        </button>
      </form>
    </main>
  );
}
