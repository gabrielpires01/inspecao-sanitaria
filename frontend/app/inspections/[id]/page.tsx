'use client';

import { useRouter, useParams } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import InspectionInfo from '@/components/InspectionInfo';
import IrregularitiesList from '@/components/IrregularitiesList';
import { useInspectionData } from '@/hooks/useInspectionData';
import { Status } from '@/lib/types';
import styles from './page.module.css';

export default function InspectionDetailPage() {
  return (
    <ProtectedRoute>
      <InspectionDetailContent />
    </ProtectedRoute>
  );
}

function InspectionDetailContent() {
  const params = useParams();
  const router = useRouter();
  const inspectionId = parseInt(params.id as string);

  const {
    inspection,
    irregularities,
    establishment,
    inspector,
    irregularityInspectors,
    loading,
    error,
  } = useInspectionData(inspectionId);

  const isFinalized = inspection
    ? [
        Status.finalized,
        Status.finalized_prohibition,
        Status.finalized_partial_prohibition,
      ].includes(inspection.status)
    : false;

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Carregando...</div>
      </div>
    );
  }

  if (error || !inspection) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>
          {error || 'Inspeção não encontrada'}
        </div>
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
        <h1>Inspeção #{inspection.id}</h1>
      </header>

      <div className={styles.content}>
        <InspectionInfo
          inspection={inspection}
          establishment={establishment || undefined}
          inspector={inspector || undefined}
        />

        <IrregularitiesList
          irregularities={irregularities}
          inspectors={irregularityInspectors}
          isFinalized={isFinalized}
          inspectionId={inspectionId}
        />

        {!isFinalized && (
          <div className={styles.section}>
            <button
              onClick={() =>
                router.push(`/inspections/${inspectionId}/finalize`)
              }
              className={styles.finalizeButton}
            >
              Finalizar Inspeção
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
