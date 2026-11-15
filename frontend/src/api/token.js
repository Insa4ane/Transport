// Token logowania trzymamy w localStorage, żeby przetrwał odświeżenie strony (F5).
const KEY = "token";

export const getToken = () => localStorage.getItem(KEY);
export const setToken = (token) => localStorage.setItem(KEY, token);
export const clearToken = () => localStorage.removeItem(KEY);
