import { AuthProvider } from "./context/AuthProvider.context";
import { LoginForm } from "./features/auth/components/LoginForm/LoginForm";
import { CreateCustomerForm } from "./features/customers/components/CreateCustomerForm/CreateCustomerForm";
import { useAuth } from "./context/AuthContext";
import "./App.css";

const AppContent = () => {
  const { isAuthenticated, isLoading, logout } = useAuth();

  if (isLoading) {
    return <div>Chargement...</div>;
  }

  if (!isAuthenticated) {
    return <LoginForm />;
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
        <CreateCustomerForm />
      </main>
    </>
  );
};

export const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};
