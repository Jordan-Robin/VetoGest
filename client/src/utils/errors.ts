import axios from "axios";

export const getAxiosErrorMessage = (
  error: unknown,
  defaultMessage: string
): string => {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.detail || defaultMessage;
  }
  return defaultMessage;
};
