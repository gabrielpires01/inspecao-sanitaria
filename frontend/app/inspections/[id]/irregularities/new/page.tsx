'use client';

import { useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import { Severity } from '@/lib/types';
import { useCreateIrregularity } from '@/hooks/queries/useIrregularities';
import FormActions from '@/components/FormActions';
import styles from './page.module.css';

const severityOptions = [
  { value: Severity.low, label: 'Baixa' },
  { value: Severity.moderate, label: 'Moderada' },
  { value: Severity.major, label: 'Alta' },
  { value: Severity.critical, label: 'Crítica' },
];

export default function NewIrregularityPage() {
  return (
    <ProtectedRoute>
      <NewIrregularityContent />
    </ProtectedRoute>
  );
}

function NewIrregularityContent() {
  const params = useParams();
  const router = useRouter();
  const inspectionId = parseInt(params.id as string);

  const [description, setDescription] = useState('');
  const [severity, setSeverity] = useState<Severity>(Severity.moderate);
  const [requiresInterruption, setRequiresInterruption] = useState(false);
  const createIrregularity = useCreateIrregularity();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!description.trim()) {
      return;
    }

    const irregularityData = {
      inspection_id: inspectionId,
      description: description.trim(),
      severity,
      requires_interruption: requiresInterruption,
    };

    createIrregularity.mutate(irregularityData, {
      onSuccess: () => {
        router.push(`/inspections/${inspectionId}`);
      },
    });
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <button onClick={() => router.back()} className={styles.backButton}>
          ← Voltar
        </button>
        <h1>Nova Irregularidade</h1>
      </header>

      <div className={styles.content}>
        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.inputGroup}>
            <label htmlFor="description">Descrição *</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Descreva a irregularidade encontrada..."
              required
              rows={6}
              className={styles.textarea}
            />
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="severity">Severidade</label>
            <select
              id="severity"
              value={severity}
              onChange={(e) =>
                setSeverity(parseInt(e.target.value) as Severity)
              }
              className={styles.select}
            >
              {severityOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div className={styles.checkboxGroup}>
            <label className={styles.checkboxLabel}>
              <input
                type="checkbox"
                checked={requiresInterruption}
                onChange={(e) => setRequiresInterruption(e.target.checked)}
                className={styles.checkbox}
              />
              <span>Requer interrupção imediata</span>
            </label>
            <p className={styles.helpText}>
              Marque esta opção se a irregularidade requer interrupção imediata
              das atividades
            </p>
          </div>

          {!description.trim() && (
            <div className={styles.error}>A descrição é obrigatória</div>
          )}
          {createIrregularity.error && (
            <div className={styles.error}>
              {(createIrregularity.error as any)?.response?.data?.detail ||
                'Erro ao criar irregularidade'}
            </div>
          )}

          <FormActions
            onCancel={() => router.back()}
            submitLabel={
              createIrregularity.isPending ? 'Criando...' : 'Criar Irregularidade'
            }
            loading={createIrregularity.isPending}
            disabled={!description.trim()}
          />
        </form>
      </div>
    </div>
  );
}
