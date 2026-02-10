import type { LoginCredentials, TokenResponse } from "@/types/auth.types";
import api from "./api";

// TODO utiliser httpOnly cookies
export const authService = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>("/token/", credentials);
    return response.data;
  },

  refreshToken: async (refresh: string): Promise<{ access: string }> => {
    const response = await api.post<{ access: string }>("/token/refresh/", {
      refresh,
    });
    return response.data;
  },

  logout: () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
  },

  getAccessToken: () => localStorage.getItem("accessToken"),
  getRefreshToken: () => localStorage.getItem("refreshToken"),

  setTokens: (access: string, refresh: string) => {
    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
  },

  isAuthenticated: () => !!localStorage.getItem("accessToken"),
};
