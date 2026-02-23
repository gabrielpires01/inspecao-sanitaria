import React from 'react';
import { useRouter } from 'next/navigation';
import type { Irregularity, User } from '@/lib/types';
import IrregularityCard from './IrregularityCard';
import styles from './IrregularitiesList.module.css';

interface IrregularitiesListProps {
  irregularities: Irregularity[];
  inspectors: Record<number, User>;
  isFinalized: boolean;
  inspectionId: number;
}

export default function IrregularitiesList({
  irregularities,
  inspectors,
  isFinalized,
  inspectionId,
}: IrregularitiesListProps) {
  const router = useRouter();

  return (
    <div className={styles.section}>
      <div className={styles.header}>
        <h2>Irregularidades</h2>
        {!isFinalized && (
          <button
            onClick={() =>
              router.push(`/inspections/${inspectionId}/irregularities/new`)
            }
            className={styles.addButton}
          >
            + Adicionar
          </button>
        )}
      </div>

      {irregularities.length === 0 ? (
        <div className={styles.empty}>Nenhuma irregularidade registrada</div>
      ) : (
        <div className={styles.list}>
          {irregularities.map((irregularity) => (
            <IrregularityCard
              key={irregularity.id}
              irregularity={irregularity}
              inspector={inspectors[irregularity.inspector_id]}
            />
          ))}
        </div>
      )}
    </div>
  );
}
