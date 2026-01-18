import type { Customer } from "@/types/customer";

interface ValidationResult {
  isValid: boolean;
  missingFields: (keyof Customer)[];
  errors: string[];
}

export const CUSTOMER_REQUIRED_FIELDS: (keyof Customer)[] = [
  "lastName",
  "firstName",
  "email",
  "phoneNumber",
  "street",
  "zipCode",
  "city",
];

export const validateCustomer = (data: Customer): ValidationResult => {
  const errors: string[] = [];

  const missingFields = CUSTOMER_REQUIRED_FIELDS.filter((field) => {
    const value = data[field];
    return (
      value === null || value === undefined || value.toString().trim() === ""
    );
  });

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (data.email && !emailRegex.test(data.email)) {
    errors.push("email_format");
  }

  // Format Téléphone (Standard français simple : 10 chiffres)
  const phoneRegex = /^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/;
  if (data.phoneNumber && !phoneRegex.test(data.phoneNumber)) {
    errors.push("phone_format");
  }

  return {
    isValid: missingFields.length === 0 && errors.length === 0,
    missingFields,
    errors,
  };
};
