import { createContext, useContext } from "react";

// Kontekst to "globalna zmienna" Reacta: każdy komponent może odczytać zalogowanego
// użytkownika przez useAuth(), bez przekazywania go ręcznie przez propsy.
export const AuthContext = createContext(null);

export function useAuth() {
  return useContext(AuthContext);
}
