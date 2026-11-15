# Wspólne przejazdy

Aplikacja webowa (Full-Stack MVP) do organizowania wspólnych przejazdów. Kierowcy dodają trasy, pasażerowie przeglądają je i rezerwują miejsca.

**Stack:** React (Vite) · FastAPI · SQLite

## Funkcje

- **Przeglądanie przejazdów bez logowania:** lista tras z filtrowaniem po miejscu startu i celu (działa też z polskimi znakami, np. „łódź" znajdzie „Łódź").
- **Rejestracja i logowanie:** login, hasło, powtórzenie hasła oraz wybór roli (kierowca / pasażer). Hasła są hashowane (bcrypt), sesja opiera się na tokenach JWT.
- **Szczegóły trasy i rezerwacja miejsc** (po zalogowaniu): niezalogowany użytkownik, który kliknie trasę, jest przekierowany do logowania, a po zalogowaniu wraca na wybraną trasę.
- **Moje rezerwacje i odwoływanie:** pasażer widzi swoje rezerwacje i może je odwołać (przycisk „Odwołaj”), a miejsca wracają do puli. Odwołać można tylko własną rezerwację i tylko przed odjazdem.
- **Dodawanie przejazdów:** tylko dla kierowców.
- **Role egzekwowane po stronie serwera:** pasażer nie doda trasy, a kierowca nie zarezerwuje miejsca (odpowiedź `403`), niezależnie od tego, co pokazuje frontend.
- **Bezpieczna rezerwacja miejsc:** liczba wolnych miejsc zmniejsza się atomowo jednym zapytaniem SQL, więc równoległe rezerwacje nie zejdą poniżej zera.

## Wymagania

- Python 3.10+
- Node.js 20.19+ lub 22+ (z npm)

## Uruchomienie

Aplikacja składa się z dwóch serwerów uruchamianych w osobnych terminalach.

### 1. Backend (port 8000)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn API.server:app --reload
```

Serwer musi być uruchamiany z katalogu `backend/`. Baza SQLite (`backend/Database/app.db`) tworzy się automatycznie przy pierwszym starcie. Interaktywna dokumentacja API jest pod adresem http://localhost:8000/docs.

### 2. Frontend (port 5173)

```bash
cd frontend
npm install
npm run dev
```

Aplikacja będzie dostępna pod adresem http://localhost:5173. Baza startuje pusta, więc zacznij od założenia konta kierowcy (żeby dodać pierwszy przejazd) i konta pasażera (żeby zarezerwować miejsce).

### Konfiguracja (opcjonalna)

Wartości domyślne są w `backend/API/config.py`. Można je nadpisać zmiennymi środowiskowymi:

| Zmienna | Znaczenie | Domyślnie |
|---|---|---|
| `SECRET_KEY` | klucz podpisujący tokeny JWT | klucz deweloperski (z ostrzeżeniem w logu) |
| `DB_PATH` | ścieżka do pliku bazy SQLite | `backend/Database/app.db` |
| `CORS_ORIGINS` | dozwolone adresy frontendu, rozdzielone przecinkami | `http://localhost:5173,http://127.0.0.1:5173` |

W środowisku produkcyjnym `SECRET_KEY` trzeba koniecznie ustawić na własną, losową wartość.

## API

Wszystkie ścieżki mają prefiks `/api`. Błędy mają postać `{"detail": "komunikat"}`.

| Metoda | Ścieżka | Dostęp | Opis |
|---|---|---|---|
| POST | `/auth/register` | publiczny | rejestracja (`username`, `password`, `is_driver`) |
| POST | `/auth/login` | publiczny | logowanie, zwraca `access_token` i dane użytkownika |
| GET | `/rides?origin=&destination=` | publiczny | lista przejazdów z opcjonalnymi filtrami |
| GET | `/rides/{id}` | zalogowany | szczegóły przejazdu |
| POST | `/rides` | kierowca | dodanie przejazdu |
| POST | `/rides/{id}/book` | pasażer | rezerwacja miejsc (`seats`) |
| GET | `/bookings` | pasażer | moje rezerwacje |
| DELETE | `/bookings/{id}` | pasażer (właściciel) | odwołanie rezerwacji, odpowiedź `204` |

Token przesyłany jest w nagłówku `Authorization: Bearer <token>`.

Kody błędów: `400` brak wolnych miejsc lub próba odwołania po odjeździe, `401` brak lub nieważny token, `403` brak uprawnień (zła rola), `404` nie znaleziono przejazdu lub rezerwacji, `409` zajęty login, `422` niepoprawne dane.

## Struktura projektu

```
backend/
├── requirements.txt
├── Database/                       warstwa danych
│   ├── connection.py               połączenie z SQLite, transakcje, blokada wątków
│   ├── schema.py                   definicje tabel
│   ├── models.py                   obiekty domenowe (User, Ride)
│   ├── exceptions.py               błędy bazy
│   └── repositories/               repozytoria: całe SQL jest tutaj
│       ├── user_repository.py
│       ├── ride_repository.py      przejazdy i atomowa rezerwacja
│       └── booking_repository.py   lista i odwoływanie rezerwacji
└── API/
    ├── server.py                   punkt wejścia: CORS, obsługa błędów, routery
    ├── config.py                   konfiguracja (stałe)
    ├── container.py                składanie obiektów aplikacji w jednym miejscu
    ├── dependencies.py             zależności FastAPI (zalogowany użytkownik, role)
    ├── errors.py                   własne błędy aplikacji
    ├── security/                   hashowanie haseł (bcrypt) i tokeny (JWT)
    ├── schemas/                    modele żądań i odpowiedzi (Pydantic)
    ├── services/                   logika: AuthService, RideService, BookingService
    └── routers/                    cienkie endpointy HTTP

frontend/src/
├── api/                            klient API (fetch) i obsługa tokenu
├── auth/                           kontekst zalogowanego użytkownika
├── components/                     nagłówek, ochrona tras
└── pages/                          lista tras, szczegóły, moje rezerwacje, logowanie, rejestracja, dodawanie trasy
```

## Decyzje projektowe

- **Warstwy:** routery → serwisy → repozytoria → baza. Endpointy nie zawierają logiki, a SQL występuje tylko w repozytoriach.
- **Wstrzykiwanie zależności:** serwisy dostają repozytoria i usługi bezpieczeństwa w konstruktorze, a obiekty składane są w `container.py`.
- **Błędy:** serwisy rzucają własne wyjątki (`NotFound`, `Forbidden`, …), a jeden handler zamienia je na odpowiedzi HTTP.
- **Bezpieczeństwo:** hasła hashowane bcryptem, ten sam komunikat dla złego loginu i złego hasła, wyrównywanie czasu odpowiedzi, tokeny z datą ważności (12 h), kierowca przy dodawaniu trasy pobierany z tokenu, a nie z żądania.
- **Daty:** przechowywane w UTC w jednym formacie, a we frontendzie wyświetlane w czasie lokalnym przeglądarki.
- **SQLite:** jedno połączenie współdzielone przez wątki FastAPI i serializowane blokadą. Wystarcza dla MVP, a przy większym ruchu warto przejść na bazę serwerową.

## Uproszczenia i ograniczenia (MVP)

- Aplikacja nie ma funkcji opartych na AI (były opcjonalne).
- Brak edycji i usuwania przejazdów oraz powiadomień dla kierowcy. Odwołana rezerwacja jest usuwana (bez historii).
- Rola jest przypisana do konta przy rejestracji. Kto chce być kierowcą i pasażerem, zakłada dwa konta.
- Token logowania jest przechowywany w `localStorage` przeglądarki i nie ma mechanizmu odświeżania tokenów.
- Brak migracji bazy. Po zmianie schematu usuń plik `backend/Database/app.db`.

## Wykorzystanie narzędzi AI

Do pracy używałem Claude. Podział był taki:

- **Claude:** Odpowiadał za wygląd w Reakcie oraz za to, jak całość ma wizualnie wyglądać i się prezentować. Generował również kod funkcji backendowych.

- **Ja:** Odpowiadałem za logikę aplikacji, architekturę oraz projekt i wygląd funkcji w backendzie. Claude generował te funkcje, a ja ewentualnie rozbijałem je na mniejsze części lub poprawiałem, dodawałem własne pomysły (np. odwoływanie rezerwacji) i modyfikowałem kod po swojemu. Do mnie należał też wybór tematu i stacku, zaprojektowanie ról (kierowca / pasażer, widok dla gościa) oraz lokalne uruchomienie i sprawdzenie projektu.