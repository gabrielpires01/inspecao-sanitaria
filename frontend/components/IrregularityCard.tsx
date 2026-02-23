import React from 'react';
import type { Irregularity, User } from '@/lib/types';
import { Severity } from '@/lib/types';
import styles from './IrregularityCard.module.css';

const severityLabels: Record<Severity, string> = {
  [Severity.low]: 'Baixa',
  [Severity.moderate]: 'Moderada',
  [Severity.major]: 'Alta',
  [Severity.critical]: 'Crítica',
  [Severity.resolved]: 'Resolvida',
};

interface IrregularityCardProps {
  irregularity: Irregularity;
  inspector?: User;
}

export default function IrregularityCard({
  irregularity,
  inspector,
}: IrregularityCardProps) {
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
    <div className={styles.card}>
      <div className={styles.header}>
        <span className={styles.id}>#{irregularity.id}</span>
        <span
          className={`${styles.severity} ${
            styles[`severity${irregularity.severity}`]
          }`}
        >
          {severityLabels[irregularity.severity]}
        </span>
        {irregularity.requires_interruption && (
          <span className={styles.interruptionBadge}>
            ⚠ Interrupção Imediata
          </span>
        )}
      </div>
      <div className={styles.description}>{irregularity.description}</div>
      <div className={styles.footer}>
        <div className={styles.meta}>
          <span className={styles.label}>Inspetor:</span>
          {inspector ? (
            <span className={styles.inspectorName}>{inspector.full_name}</span>
          ) : (
            <span className={styles.loading}>Carregando...</span>
          )}
        </div>
        <div className={styles.date}>
          Criada em: {formatDate(irregularity.created_at)}
        </div>
      </div>
    </div>
  );
}
