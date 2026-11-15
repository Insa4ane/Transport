import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || "/";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault(); 
    setError("");
    setSubmitting(true);
    try {
      await login(username.trim(), password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  }

  return (
    <main className="narrow">
      <h1>Logowanie</h1>
      {location.state?.from && (
        <p className="notice">Aby kontynuować, musisz się zalogować.</p>
      )}

      <form onSubmit={handleSubmit} className="form">
        <label>
          Login
          <input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus required />
        </label>
        <label>
          Hasło
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit" className="btn" disabled={submitting}>
          {submitting ? "Logowanie…" : "Zaloguj się"}
        </button>
      </form>

      <p className="form-footer">
        Nie masz konta? <Link to="/register" state={location.state}>Zarejestruj się</Link>
      </p>
    </main>
  );
}
