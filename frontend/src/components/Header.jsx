import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <header className="header">
      <Link to="/" className="logo">🚗 Wspólne przejazdy</Link>

      <nav className="header-right">
        {user ? (
          <>
            {user.is_driver ? (
              <Link to="/rides/new">Dodaj przejazd</Link>
            ) : (
              <Link to="/bookings">Moje rezerwacje</Link>
            )}
            <span className="user-badge">
              {user.username} · {user.is_driver ? "kierowca" : "pasażer"}
            </span>
            <button className="btn btn-secondary" onClick={handleLogout}>
              Wyloguj się
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Zaloguj się</Link>
            <Link to="/register" className="btn">Zarejestruj się</Link>
          </>
        )}
      </nav>
    </header>
  );
}
