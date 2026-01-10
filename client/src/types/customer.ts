export interface Customer {
  id?: number;
  lastName: string;
  firstName: string;
  email: string;
  phoneNumber: string;
  street: string;
  zipCode: string;
  city: string;
  description?: string;
  archive?: boolean;
  readonly createdAt?: string;
  readonly updatedAt?: string;
}