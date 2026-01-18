import { describe, it, expect } from "vitest";
import { validateCustomer } from "./customerValidator";
import type { Customer } from "@/types/customer";

describe("validateCustomer", () => {
  it("devrait retourner isValid: true", () => {
    const validCustomer: Customer = {
      lastName: "Dupont",
      firstName: "Jean",
      email: "jean@example.com",
      phoneNumber: "0102030405",
      street: "1 rue de la Paix",
      zipCode: "75001",
      city: "Paris",
      description: "Un client sympa",
    };

    const result = validateCustomer(validCustomer);

    expect(result.isValid).toBe(true);
    expect(result.missingFields).toHaveLength(0);
  });

  it("devrait retourner isValid: false et lister les champs manquants", () => {
    const incompleteData: Partial<Customer> = {
      lastName: "Dupont",
      firstName: "",
      email: "jean@example.com",
    };

    const result = validateCustomer(incompleteData as Customer);

    expect(result.isValid).toBe(false);
    expect(result.missingFields).toContain("firstName");
    expect(result.missingFields).toContain("street");
    expect(result.missingFields).toContain("city");
    expect(result.missingFields).not.toContain("lastName");
  });

  it("devrait gérer les chaînes de caractères composées uniquement d'espaces", () => {
    const spaceData: Customer = {
      lastName: "   ",
      firstName: "Jean",
      email: "jean@example.com",
      phoneNumber: "0102030405",
      street: "1 rue de la Paix",
      zipCode: "75001",
      city: "Paris",
    };

    const result = validateCustomer(spaceData);

    expect(result.isValid).toBe(false);
    expect(result.missingFields).toContain("lastName");
  });
});
