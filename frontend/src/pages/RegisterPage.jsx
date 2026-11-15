import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || "/";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [role, setRole] = useState("passenger"); 
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    // Walidacja po stronie frontendu (to tylko wygoda; backend waliduje też).
    if (username.trim().length < 3) return setError("Login musi mieć co najmniej 3 znaki");
    if (password.length < 8) return setError("Hasło musi mieć co najmniej 8 znaków");
    if (password !== password2) return setError("Hasła nie są takie same");

    setSubmitting(true);
    try {
      await register(username.trim(), password, role === "driver");
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  }

  return (
    <main className="narrow">
      <h1>Rejestracja</h1>

      <form onSubmit={handleSubmit} className="form">
        <label>
          Login
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus required />
        </label>
        <label>
          Hasło
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        <label>
          Powtórz hasło
          <input type="password" value={password2} onChange={(e) => setPassword2(e.target.value)} required />
        </label>

        <fieldset>
          <legend>Kim jesteś?</legend>
          <label className="radio">
            <input
              type="radio"
              name="role"
              value="passenger"
              checked={role === "passenger"}
              onChange={(e) => setRole(e.target.value)}
            />
            Pasażer (rezerwuję przejazdy)
          </label>
          <label className="radio">
            <input
              type="radio"
              name="role"
              value="driver"
              checked={role === "driver"}
              onChange={(e) => setRole(e.target.value)}
            />
            Kierowca (dodaję przejazdy)
          </label>
        </fieldset>

        {error && <p className="error">{error}</p>}
        <button type="submit" className="btn" disabled={submitting}>
          {submitting ? "Rejestrowanie…" : "Zarejestruj się"}
        </button>
      </form>

      <p className="form-footer">
        Masz już konto? <Link to="/login" state={location.state}>Zaloguj się</Link>
      </p>
    </main>
  );
}
