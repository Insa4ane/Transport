import { useState } from "react";
import { AuthContext } from "./AuthContext";
import { api } from "../api";
import { setToken, clearToken } from "../api/token";

const USER_KEY = "user";

function loadUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY));
  } catch {
    return null;
  }
}

export default function AuthProvider({ children }) {
  // Startowa wartość z localStorage, więc po F5 użytkownik zostaje zalogowany.
  const [user, setUser] = useState(loadUser);

  async function login(username, password) {
    const { access_token, user } = await api.login({ username, password });
    setToken(access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
    setUser(user);
  }

  async function register(username, password, isDriver) {
    await api.register({ username, password, is_driver: isDriver });
    await login(username, password); // po rejestracji od razu logujemy
  }

  function logout() {
    clearToken();
    localStorage.removeItem(USER_KEY);
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
