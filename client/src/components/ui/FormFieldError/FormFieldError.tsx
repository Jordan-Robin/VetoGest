import styles from "./FormFieldError.module.css";
import { AlertCircle } from "lucide-react";

interface FormFieldErrorProps {
  message?: string;
  fieldId?: string;
}

export const FormFieldError = ({ message, fieldId }: FormFieldErrorProps) => {
  if (!message) return null;

  return (
    <div
      className={styles.errorContainer}
      id={fieldId ? `${fieldId}-error` : undefined}
      role="alert"
    >
      <AlertCircle size={16} />
      <span>{message}</span>
    </div>
  );
};
