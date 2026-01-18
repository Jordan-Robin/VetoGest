import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { CreateCustomerForm } from "./CreateCustomerForm";
import { customerService } from "@/features/customers/services/customerService";

// Simulation du service
vi.mock("@/features/customers/services/customerService", () => ({
  customerService: {
    create: vi.fn(),
  },
}));

describe("CreateCustomerForm - Tests d'intégration", () => {
  // Formulaire correctement completé
  it("affiche un message de succès et vide le formulaire après une création réussie", async () => {
    const mockCustomer = {
      id: 1,
      lastName: "Dupont",
      firstName: "Jean",
      email: "jean.dupont@gmail.com",
      phoneNumber: "0601020304",
      street: "10 rue de Paris",
      zipCode: "75001",
      city: "Paris",
      description: "Client test",
      createdAt: "2024-01-01T00:00:00Z",
      updatedAt: "2024-01-01T00:00:00Z",
    };

    vi.mocked(customerService.create).mockResolvedValueOnce(mockCustomer);

    render(<CreateCustomerForm />);

    fireEvent.change(screen.getByLabelText(/^Nom/i), {
      target: { value: "Dupont" },
    });
    fireEvent.change(screen.getByLabelText(/E-mail/i), {
      target: { value: "jean.dupont@gmail.com" },
    });
    fireEvent.change(screen.getByLabelText(/Prénom/i), {
      target: { value: "Jean" },
    });
    fireEvent.change(screen.getByLabelText(/Téléphone/i), {
      target: { value: "0601020304" },
    });
    fireEvent.change(screen.getByLabelText(/Rue/i), {
      target: { value: "10 rue de Paris" },
    });
    fireEvent.change(screen.getByLabelText(/Code Postal/i), {
      target: { value: "75001" },
    });
    fireEvent.change(screen.getByLabelText(/Ville/i), {
      target: { value: "Paris" },
    });
    fireEvent.change(screen.getByLabelText(/Description \/ notes/i), {
      target: { value: "Client test" },
    });

    fireEvent.click(screen.getByRole("button", { name: /créer le client/i }));

    const successMessage = await screen.findByText(
      /Le client Jean Dupont a été créé !/i
    );
    expect(successMessage).toBeInTheDocument();

    expect(screen.getByLabelText(/^Nom/i)).toHaveValue("");
    expect(screen.getByLabelText(/E-mail/i)).toHaveValue("");
  });

  // Soumission du formulaire alors qu'aucun champ n'est rempli
  it("affiche les messages d'erreur obligatoires lors d'une soumission vide", async () => {
    render(<CreateCustomerForm />);

    fireEvent.click(screen.getByRole("button", { name: /créer le client/i }));

    expect(
      await screen.findByText(/Le champ 'Nom' est obligatoire/i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Le champ 'E-mail' est obligatoire/i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Merci de corriger les erreurs/i)
    ).toBeInTheDocument();
  });
});
