import React from 'react';
import type { Inspection, Establishment, User } from '@/lib/types';
import { Status } from '@/lib/types';
import styles from './InspectionInfo.module.css';

const statusLabels: Record<Status, string> = {
  [Status.clear]: 'Autorizada',
  [Status.has_irregularities]: 'Com Irregularidades',
  [Status.immediate_prohibition]: 'Interdição Imediata',
  [Status.finalized]: 'Finalizada',
  [Status.finalized_prohibition]: 'Finalizada com Interdição',
  [Status.finalized_partial_prohibition]: 'Finalizada com Interdição Parcial',
};

interface InspectionInfoProps {
  inspection: Inspection;
  establishment?: Establishment;
  inspector?: User;
}

export default function InspectionInfo({
  inspection,
  establishment,
  inspector,
}: InspectionInfoProps) {
  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Não informada';
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className={styles.section}>
      <h2>Informações</h2>
      <div className={styles.infoGrid}>
        <div className={styles.infoItem}>
          <strong>Estabelecimento:</strong>{' '}
          {establishment ? (
            <span className={styles.establishmentName}>
              {establishment.name}
            </span>
          ) : (
            <span className={styles.loading}>Carregando...</span>
          )}
        </div>
        <div className={styles.infoItem}>
          <strong>Inspetor:</strong>{' '}
          {inspector ? (
            <span className={styles.inspectorName}>{inspector.full_name}</span>
          ) : (
            <span className={styles.loading}>Carregando...</span>
          )}
        </div>
        <div className={styles.infoItem}>
          <strong>Status:</strong>
          <span
            className={`${styles.status} ${
              styles[`status${inspection.status}`]
            }`}
          >
            {statusLabels[inspection.status]}
          </span>
        </div>
        <div className={styles.infoItem}>
          <strong>Data/Hora:</strong> {formatDate(inspection.date_time)}
        </div>
        <div className={styles.infoItem}>
          <strong>Criada em:</strong> {formatDate(inspection.created_at)}
        </div>
      </div>
    </div>
  );
}
