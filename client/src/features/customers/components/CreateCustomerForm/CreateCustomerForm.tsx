import React, { useState } from "react";
import type { Customer } from "@/types/customer";
import { customerService } from "@/features/customers/services/customerService";
import { validateCustomer } from "@/features/customers/utils/customerValidator";
import { getAxiosErrorMessage } from "@/utils/errors";
import { FormField } from "@/components/ui/FormField/FormField";

// Mapping des labels
const LABELS: Partial<Record<keyof Customer, string>> = {
  lastName: "Nom",
  firstName: "Prénom",
  email: "E-mail",
  phoneNumber: "Téléphone",
  street: "Rue",
  zipCode: "Code Postal",
  city: "Ville",
  description: "Description / notes",
};

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
  const [fieldErrors, setFieldErrors] = useState<
    Partial<Record<keyof Customer, string>>
  >({});
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

    // Nettoyer l'erreur du champ en cours de modification
    if (fieldErrors[name as keyof Customer]) {
      setFieldErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  // Soumission du formulaire
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFieldErrors({});

    // Validation du formulaire
    const { isValid, missingFields, errors } = validateCustomer(formData);

    if (!isValid) {
      const newFieldErrors: typeof fieldErrors = {};

      // Gestion des champs obligatoires manquants
      missingFields.forEach((field) => {
        newFieldErrors[field] = `Le champ '${
          LABELS[field] || field
        }' est obligatoire.`;
      });

      // Gestion des erreurs spécifiques (format)
      if (errors.includes("email_format")) {
        newFieldErrors.email = "Le format de l'adresse email est incorrect.";
      }
      if (errors.includes("phone_format")) {
        newFieldErrors.phoneNumber =
          "Le numéro de téléphone doit contenir 10 chiffres.";
      }

      setFieldErrors(newFieldErrors);
      setStatus({
        type: "error",
        message: "Merci de corriger les erreurs dans le formulaire.",
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

      <form onSubmit={handleSubmit} className="client-form" noValidate>
        <FormField
          name="lastName"
          value={formData.lastName}
          onChange={handleChange}
          placeholder="Dupont"
          required
          label={LABELS.lastName}
          error={fieldErrors.lastName}
        />

        <FormField
          name="firstName"
          value={formData.firstName}
          onChange={handleChange}
          placeholder="Jean"
          required
          label={LABELS.firstName}
          error={fieldErrors.firstName}
        />

        <FormField
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="jean.dupont@email.com"
          required
          label={LABELS.email}
          error={fieldErrors.email}
        />

        <FormField
          name="phoneNumber"
          value={formData.phoneNumber}
          onChange={handleChange}
          placeholder="06 12 34 56 78"
          required
          label={LABELS.phoneNumber}
          error={fieldErrors.phoneNumber}
        />

        <FormField
          name="street"
          value={formData.street}
          onChange={handleChange}
          placeholder="123 Rue de la République"
          required
          label={LABELS.street}
          error={fieldErrors.street}
        />

        <div className="form-row">
          <FormField
            name="zipCode"
            value={formData.zipCode}
            onChange={handleChange}
            placeholder="56200"
            required
            label={LABELS.zipCode}
            error={fieldErrors.zipCode}
          />

          <FormField
            name="city"
            value={formData.city}
            onChange={handleChange}
            placeholder="Glénac"
            required
            label={LABELS.city}
            error={fieldErrors.city}
          />
        </div>

        <FormField
          isTextArea
          name="description"
          value={formData.description || ""}
          onChange={handleChange}
          label={LABELS.description}
          maxLength={200}
          error={fieldErrors.description}
        />

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Envoi..." : "Créer le Client"}
        </button>
      </form>
    </div>
  );
};
