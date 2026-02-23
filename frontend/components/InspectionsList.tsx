import React from 'react';
import type { Inspection, Establishment, User } from '@/lib/types';
import InspectionCard from './InspectionCard';
import styles from './InspectionsList.module.css';

interface InspectionsListProps {
  inspections: Inspection[];
  establishments: Record<number, Establishment>;
  inspectors: Record<number, User>;
}

export default function InspectionsList({
  inspections,
  establishments,
  inspectors,
}: InspectionsListProps) {
  if (inspections.length === 0) {
    return (
      <div className={styles.empty}>Nenhuma inspeção encontrada</div>
    );
  }

  return (
    <div className={styles.list}>
      {inspections.map((inspection) => (
        <InspectionCard
          key={inspection.id}
          inspection={inspection}
          establishment={establishments[inspection.establishment_id]}
          inspector={inspectors[inspection.inspector_id]}
        />
      ))}
    </div>
  );
}
