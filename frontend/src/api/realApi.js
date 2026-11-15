// Prawdziwe API (FastAPI). Poniżej KONTRAKT, który ma spełnić backend.
//
//  POST /api/auth/register   {username, password, is_driver}      -> 201 {id, username, is_driver}
//  POST /api/auth/login      {username, password}                 -> {access_token, user:{id, username, is_driver}}
//  GET  /api/rides?origin=&destination=                           -> [ride]            (publiczne)
//  GET  /api/rides/{id}                                           -> ride              (wymaga tokenu)
//  POST /api/rides           {origin, destination, departure,
//                             seats, price}                       -> 201 ride          (tylko kierowca, inaczej 403)
//  POST /api/rides/{id}/book {seats}                              -> ride              (tylko pasażer, inaczej 403;
//                                                                                       brak miejsc -> 400)
//  GET  /api/bookings                                             -> [booking]         (tylko pasażer)
//  DELETE /api/bookings/{id}                                      -> 204               (tylko właściciel rezerwacji;
//                                                                                       po odjeździe -> 400)
//
//  booking = {id, seats, ride_id, origin, destination, departure, price, driver_name}
//  ride = {id, origin, destination, departure (ISO 8601), seats_left, price, driver_name}
//  Token wysyłamy w nagłówku:  Authorization: Bearer <access_token>
//  Błędy: JSON {"detail": "tekst"} (tak odpowiada FastAPI przy HTTPException).

import { getToken } from "./token";

const BASE = "http://localhost:8000/api";

function errorMessage(data, status) {
  const detail = data?.detail;
  if (typeof detail === "string") return detail;
  // FastAPI przy walidacji (422) zwraca listę błędów
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join("; ");
  return `Błąd serwera (${status})`;
}

async function request(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  let res;
  try {
    res = await fetch(`${BASE}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new Error("Nie można połączyć się z serwerem. Czy backend działa?");
  }

  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(errorMessage(data, res.status));
  return data;
}

export const realApi = {
  register: (data) => request("/auth/register", { method: "POST", body: data }),
  login: (data) => request("/auth/login", { method: "POST", body: data }),
  getRides: ({ origin = "", destination = "" } = {}) => {
    const params = new URLSearchParams();
    if (origin) params.set("origin", origin);
    if (destination) params.set("destination", destination);
    const qs = params.toString();
    return request(`/rides${qs ? `?${qs}` : ""}`);
  },
  getRide: (id) => request(`/rides/${id}`),
  createRide: (data) => request("/rides", { method: "POST", body: data }),
  bookRide: (id, seats) =>
    request(`/rides/${id}/book`, { method: "POST", body: { seats } }),
  getMyBookings: () => request("/bookings"),
  cancelBooking: (id) => request(`/bookings/${id}`, { method: "DELETE" }),
};
