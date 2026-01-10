import React, { useState } from "react";
import type { Customer } from "@/types/customer";
import { customerService } from "@/features/customers/services/customerService";
import { validateCustomer } from "@/features/customers/utils/customerValidator";
import { getAxiosErrorMessage } from "@/utils/errors";

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
      // Envoi des données au serveur
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
        <div className="form-group">
          <label htmlFor="lastName">Nom *</label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
            placeholder="Dupont"
          />
        </div>

        <div className="form-group">
          <label htmlFor="firstName">Prénom *</label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
            placeholder="Jean"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="jean.dupont@email.com"
          />
        </div>

        <div className="form-group">
          <label htmlFor="phoneNumber">Téléphone *</label>
          <input
            type="tel"
            id="phoneNumber"
            name="phoneNumber"
            value={formData.phoneNumber}
            onChange={handleChange}
            required
            placeholder="06 12 34 56 78"
          />
        </div>

        <div className="form-group">
          <label htmlFor="street">Rue</label>
          <input
            type="text"
            id="street"
            name="street"
            value={formData.street}
            onChange={handleChange}
            placeholder="123 Rue de la République"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="zipCode">Code Postal</label>
            <input
              type="text"
              id="zipCode"
              name="zipCode"
              value={formData.zipCode}
              onChange={handleChange}
              placeholder="75001"
              maxLength={10}
            />
          </div>

          <div className="form-group">
            <label htmlFor="city">Ville</label>
            <input
              type="text"
              id="city"
              name="city"
              value={formData.city}
              onChange={handleChange}
              placeholder="Paris"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="description">Notes</label>
          <textarea
            id="description"
            name="description"
            maxLength={200}
            value={formData.description}
            onChange={handleChange}
          ></textarea>
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Envoi..." : "Créer le Client"}
        </button>
      </form>
    </div>
  );
};
