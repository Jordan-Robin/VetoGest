import styles from "./FormField.module.css";

interface FormFieldProps {
  name: string;
  type?: string;
  value: string;
  onChange: (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => void;
  placeholder?: string;
  required?: boolean;
  isTextArea?: boolean;
  label?: string;
  id?: string;
  maxLength?: number;
  error?: string;
}

export const FormField = ({
  name,
  type = "text",
  value,
  onChange,
  placeholder,
  required,
  isTextArea,
  label,
  id,
  maxLength,
  error,
}: FormFieldProps) => {
  const fieldId = id || name;
  const displayLabel = label || name.charAt(0).toUpperCase() + name.slice(1);

  return (
    <div className={styles.formGroup}>
      <label htmlFor={fieldId} className={styles.label}>
        {displayLabel} {required && "*"}
      </label>

      {isTextArea ? (
        <textarea
          id={fieldId}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          maxLength={maxLength}
          className={
            error ? `${styles.textarea} ${styles.error}` : styles.textarea
          }
          aria-invalid={error ? "true" : "false"}
          aria-describedby={error ? `${fieldId}-error` : undefined}
        />
      ) : (
        <input
          type={type}
          id={fieldId}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          maxLength={maxLength}
          className={error ? `${styles.input} ${styles.error}` : styles.input}
          aria-invalid={error ? "true" : "false"}
          aria-describedby={error ? `${fieldId}-error` : undefined}
        />
      )}

      {error && (
        <span id={`${fieldId}-error`} className={styles.errorMessage}>
          {error}
        </span>
      )}
    </div>
  );
};
