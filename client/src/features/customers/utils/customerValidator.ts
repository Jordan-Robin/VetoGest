import type { Customer } from '@/types/customer';

export const CUSTOMER_REQUIRED_FIELDS: (keyof Customer)[] = [
  'lastName',
  'firstName',
  'email',
  'phoneNumber',
  'street',
  'zipCode',
  'city'
];

export const validateCustomer = (data: Customer) => {
  const missingFields = CUSTOMER_REQUIRED_FIELDS.filter(field => {
    const value = data[field];
    return value === null || value === undefined || value.toString().trim() === '';
  });

  return {
    isValid: missingFields.length === 0,
    missingFields
  };
};