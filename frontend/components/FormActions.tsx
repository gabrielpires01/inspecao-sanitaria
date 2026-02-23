import React from 'react';
import styles from './FormActions.module.css';

interface FormActionsProps {
  onCancel: () => void;
  submitLabel: string;
  cancelLabel?: string;
  loading?: boolean;
  disabled?: boolean;
}

export default function FormActions({
  onCancel,
  submitLabel,
  cancelLabel = 'Cancelar',
  loading = false,
  disabled = false,
}: FormActionsProps) {
  return (
    <div className={styles.actions}>
      <button
        type="button"
        onClick={onCancel}
        className={styles.cancelButton}
      >
        {cancelLabel}
      </button>
      <button
        type="submit"
        disabled={loading || disabled}
        className={styles.submitButton}
      >
        {loading ? 'Processando...' : submitLabel}
      </button>
    </div>
  );
}
