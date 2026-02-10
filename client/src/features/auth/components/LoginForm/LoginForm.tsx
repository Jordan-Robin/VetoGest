import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { FormField } from "@/components/ui/FormField/FormField";
import { getAxiosErrorMessage } from "@/utils/errors";
import styles from "./LoginForm.module.css";

export const LoginForm: React.FC = () => {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Veuillez remplir tous les champs.");
      return;
    }

    setIsSubmitting(true);

    try {
      await login({ email, password });
    } catch (err) {
      const message = getAxiosErrorMessage(
        err,
        "Identifiants incorrects. Veuillez réessayer.",
      );
      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.loginContainer}>
      <h2>Connexion</h2>

      {error && <div className={styles.errorMessage}>{error}</div>}

      <form onSubmit={handleSubmit} className={styles.loginForm} noValidate>
        <FormField
          name="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="exemple@vetogest.fr"
          required
          label="Email"
        />

        <FormField
          name="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          required
          label="Mot de passe"
        />

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Connexion..." : "Se connecter"}
        </button>
      </form>
    </div>
  );
};
