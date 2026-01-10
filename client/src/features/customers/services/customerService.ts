import api from "@/services/api";
import type { Customer } from "@/types/customer";

export const customerService = {
  // Créer un client
  create: async (customer: Customer) => {
    const response = await api.post<Customer>("/customers/", customer);
    return response.data;
  },
};
