'use client';

import { useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import { FinalizeStatus } from '@/lib/types';
import { useInspection, useFinalizeInspection } from '@/hooks/queries/useInspections';
import FormActions from '@/components/FormActions';
import styles from './page.module.css';

const finalizeStatusOptions = [
  { value: FinalizeStatus.accordingly, label: 'Conforme' },
  { value: FinalizeStatus.with_problems, label: 'Com Problemas' },
  { value: FinalizeStatus.partial_prohibition, label: 'Interdição Parcial' },
  { value: FinalizeStatus.prohibition, label: 'Interdição Total' },
];

export default function FinalizeInspectionPage() {
  return (
    <ProtectedRoute>
      <FinalizeInspectionContent />
    </ProtectedRoute>
  );
}

function FinalizeInspectionContent() {
  const params = useParams();
  const router = useRouter();
  const inspectionId = parseInt(params.id as string);

  const {
    data: inspection,
    isLoading: loadingInspection,
    error: errorInspection,
  } = useInspection(inspectionId);

  const [status, setStatus] = useState<FinalizeStatus>(
    FinalizeStatus.accordingly
  );
  const [pendingIssues, setPendingIssues] = useState('');
  const finalizeInspection = useFinalizeInspection();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!pendingIssues.trim()) {
      return;
    }

    const finalizeData = {
      inspection_id: inspectionId,
      status,
      pending_issues: pendingIssues.trim(),
    };

    finalizeInspection.mutate(finalizeData, {
      onSuccess: () => {
        router.push(`/inspections/${inspectionId}`);
      },
    });
  };

  if (loadingInspection) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Carregando...</div>
      </div>
    );
  }

  if (errorInspection && !inspection) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>Erro ao carregar inspeção</div>
        <button onClick={() => router.back()} className={styles.backButton}>
          Voltar
        </button>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <button onClick={() => router.back()} className={styles.backButton}>
          ← Voltar
        </button>
        <h1>Finalizar Inspeção #{inspectionId}</h1>
      </header>

      <div className={styles.content}>
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.warning}>
            <strong>⚠️ Atenção:</strong> Ao finalizar a inspeção, não será
            possível adicionar ou modificar irregularidades.
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="status">Status de Finalização</label>
            <select
              id="status"
              value={status}
              onChange={(e) =>
                setStatus(parseInt(e.target.value) as FinalizeStatus)
              }
              className={styles.select}
            >
              {finalizeStatusOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="pendingIssues">Questões Pendentes *</label>
            <textarea
              id="pendingIssues"
              value={pendingIssues}
              onChange={(e) => setPendingIssues(e.target.value)}
              placeholder="Descreva as questões pendentes ou observações finais..."
              required
              rows={8}
              className={styles.textarea}
            />
            <p className={styles.helpText}>
              Este campo é obrigatório e deve conter informações sobre questões
              pendentes ou observações finais da inspeção.
            </p>
          </div>

          {!pendingIssues.trim() && (
            <div className={styles.error}>
              O campo "Questões Pendentes" é obrigatório
            </div>
          )}
          {finalizeInspection.error && (
            <div className={styles.error}>
              {(finalizeInspection.error as any)?.response?.data?.detail ||
                'Erro ao finalizar inspeção'}
            </div>
          )}

          <FormActions
            onCancel={() => router.back()}
            submitLabel={
              finalizeInspection.isPending ? 'Finalizando...' : 'Finalizar Inspeção'
            }
            loading={finalizeInspection.isPending}
            disabled={!pendingIssues.trim()}
          />
        </form>
      </div>
    </div>
  );
}
