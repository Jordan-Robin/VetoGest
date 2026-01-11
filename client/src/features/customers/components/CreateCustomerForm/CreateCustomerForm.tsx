import React, { useState } from "react";
import type { Customer } from "@/types/customer";
import { customerService } from "@/features/customers/services/customerService";
import { validateCustomer } from "@/features/customers/utils/customerValidator";
import { getAxiosErrorMessage } from "@/utils/errors";
import { FormField } from "@/components/ui/FormField/FormField";

// Initialisation de l'objet Customer
const initialFormData: Customer = {
  lastName: "",
  firstName: "",
  email: "",
  phoneNumber: "",
  street: "",
  zipCode: "",
  city: "",
  description: "",
};

// Composant du formulaire de création d'un Customer
export const CreateCustomerForm: React.FC = () => {
  const [formData, setFormData] = useState<Customer>(initialFormData);
  const [status, setStatus] = useState<{
    type: "success" | "error" | "";
    message: string;
  }>({ type: "", message: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Mise à jour de l'objet Customer lors d'une saisie de champ par l'utilisateur
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Soumission du formulaire
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation des champs obligatoires
    const { isValid } = validateCustomer(formData);
    if (!isValid) {
      setStatus({
        type: "error",
        message: "Veuillez remplir tous les champs obligatoires (*).",
      });
      return;
    }

    setIsSubmitting(true);
    setStatus({ type: "", message: "" });

    try {
      // Envoi des données au serveur avec gestion des erreurs
      const data = await customerService.create(formData);
      console.log("🚀 [Success] Client créé avec ID: ", data.id);
      setStatus({
        type: "success",
        message: `Le client ${data.firstName} ${data.lastName} a été créé !`,
      });
      setFormData(initialFormData);
    } catch (error) {
      console.error("❌ [Submit Error]", error);
      const serverMessage = getAxiosErrorMessage(
        error,
        "Impossible de créer le client. Vérifiez la connexion."
      );
      setStatus({ type: "error", message: serverMessage });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="client-form-container">
      <h2>Nouveau Client</h2>

      {status.message && (
        <div className={`status-message ${status.type}`}>{status.message}</div>
      )}

      <form onSubmit={handleSubmit} className="client-form">
        <FormField
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          placeholder="Dupont"
          required
          label="Nom"
        />

        <FormField
          name="firstName"
          value={formData.firstName}
          onChange={handleChange}
          placeholder="Jean"
          required
          label="Prénom"
        />

        <FormField
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="jean.dupont@email.com"
          required
          label="Email"
        />

        <FormField
          name="phoneNumber"
          value={formData.phoneNumber}
          onChange={handleChange}
          placeholder="06 12 34 56 78"
          required
          label="Téléphone"
        />

        <FormField
          name="street"
          value={formData.street}
          onChange={handleChange}
          placeholder="123 Rue de la République"
          required
          label="Rue"
        />

        <div className="form-row">
          <FormField
            name="zipCode"
            value={formData.zipCode}
            onChange={handleChange}
            placeholder="56200"
            required
            label="Code Postal"
          />

          <FormField
            name="city"
            value={formData.city}
            onChange={handleChange}
            placeholder="Glénac"
            required
            label="Ville"
          />
        </div>

        <FormField
          isTextArea
          name="description"
          value={formData.description || ""}
          onChange={handleChange}
          placeholder="Glénac"
          label="Description / notes"
          maxLength={200}
        />

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Envoi..." : "Créer le Client"}
        </button>
      </form>
    </div>
  );
};
