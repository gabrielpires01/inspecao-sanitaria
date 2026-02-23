'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import { Status } from '@/lib/types';
import { useEstablishmentSearch } from '@/hooks/useEstablishmentSearch';
import { useCreateInspection } from '@/hooks/queries/useInspections';
import EstablishmentSearch from '@/components/EstablishmentSearch';
import FormActions from '@/components/FormActions';
import styles from './page.module.css';

const statusOptions = [
  { value: Status.clear, label: 'Livre' },
  { value: Status.has_irregularities, label: 'Com Irregularidades' },
  { value: Status.immediate_prohibition, label: 'Interdição Imediata' },
];

export default function NewInspectionPage() {
  return (
    <ProtectedRoute>
      <NewInspectionContent />
    </ProtectedRoute>
  );
}

function NewInspectionContent() {
  const router = useRouter();
  const {
    search,
    setSearch,
    establishments,
    selected,
    setSelected,
    onClear,
    searching,
  } = useEstablishmentSearch();

  const [dateTime, setDateTime] = useState('');
  const [status, setStatus] = useState<Status>(Status.clear);
  const createInspection = useCreateInspection();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selected) {
      return;
    }

    let dateTimeISO = undefined;
    if (dateTime) {
      const date = new Date(dateTime);
      dateTimeISO = date.toISOString();
    }
    const inspectionData = {
      establishment_id: selected.id,
      date_time: dateTimeISO,
      status,
    };

    createInspection.mutate(inspectionData, {
      onSuccess: (inspection: { id: number }) => {
        router.push(`/inspections/${inspection.id}`);
      },
    });
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <button onClick={() => router.back()} className={styles.backButton}>
          ← Voltar
        </button>
        <h1>Nova Inspeção</h1>
      </header>

      <div className={styles.content}>
        <form onSubmit={handleSubmit} className={styles.form}>
          <EstablishmentSearch
            value={search}
            onChange={setSearch}
            establishments={establishments}
            selected={selected}
            onSelect={setSelected}
            onClear={onClear}
            searching={searching}
          />

          <div className={styles.inputGroup}>
            <label htmlFor="dateTime">Data e Hora (opcional)</label>
            <input
              id="dateTime"
              type="datetime-local"
              value={dateTime}
              onChange={(e) => setDateTime(e.target.value)}
              className={styles.input}
            />
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="status">Status</label>
            <select
              id="status"
              value={status}
              onChange={(e) => setStatus(parseInt(e.target.value) as Status)}
              className={styles.select}
            >
              {statusOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          {createInspection.error && (
            <div className={styles.error}>
              {(createInspection.error as any)?.response?.data?.detail ||
                'Erro ao criar inspeção'}
            </div>
          )}

          <FormActions
            onCancel={() => router.back()}
            submitLabel={createInspection.isPending ? 'Criando...' : 'Criar Inspeção'}
            loading={createInspection.isPending}
            disabled={!selected}
          />
        </form>
      </div>
    </div>
  );
}
