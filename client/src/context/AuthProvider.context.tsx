import React, { useState, useEffect, type ReactNode } from "react";
import { authService } from "@/services/authentication";
import type { LoginCredentials } from "@/types/auth.types";
import { AuthContext } from "./AuthContext";

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return !!authService.getAccessToken();
  });
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const handleAuthError = () => {
      setIsAuthenticated(false);
    };

    window.addEventListener("auth-error", handleAuthError);
    return () => window.removeEventListener("auth-error", handleAuthError);
  }, []);

  // TODO récupérer l'utilisateur connecté
  const login = async (credentials: LoginCredentials) => {
    const tokens = await authService.login(credentials);
    authService.setTokens(tokens.access, tokens.refresh);
    setIsAuthenticated(true);
  };

  const logout = () => {
    authService.logout();
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
