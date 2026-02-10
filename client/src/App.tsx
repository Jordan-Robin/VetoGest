import { Outlet, Navigate, useLocation } from "react-router-dom";
import { AuthProvider } from "./context/AuthProvider.context";
import { useAuth } from "./context/AuthContext";
import "./App.css";
import { PATHS } from "./routing/routingPaths";

const AppContent = () => {
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();

  if (!isAuthenticated && location.pathname !== `/${PATHS.LOGIN}`) {
    return <Navigate to={PATHS.LOGIN} replace />;
  }

  if (isAuthenticated && location.pathname === `/${PATHS.LOGIN}`) {
    return <Navigate to={PATHS.HOME} replace />;
  }

  return (
    <>
      <header>
        <h1>VetoGest</h1>
        <button onClick={logout} className="logout-btn">
          Déconnexion
        </button>
      </header>
      <main>
        <Outlet />
      </main>
    </>
  );
};

export const App = () => (
  <AuthProvider>
    <AppContent />
  </AuthProvider>
);
