'use client';

import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useAuth } from '@/contexts/AuthContext';
import { useInspectionsData } from '@/hooks/useInspectionsData';
import InspectionsList from '@/components/InspectionsList';
import styles from './page.module.css';

export default function Home() {
  return (
    <ProtectedRoute>
      <HomeContent />
    </ProtectedRoute>
  );
}

function HomeContent() {
  const { logout } = useAuth();
  const router = useRouter();
  const {
    inspections,
    establishments,
    inspectors,
    loading,
    error,
  } = useInspectionsData();

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Inspeções</h1>
        <button onClick={logout} className={styles.logoutButton}>
          Sair
        </button>
      </header>

      <div className={styles.actions}>
        <button
          onClick={() => router.push('/inspections/new')}
          className={styles.newButton}
        >
          + Nova Inspeção
        </button>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      {loading ? (
        <div className={styles.loading}>Carregando...</div>
      ) : (
        <InspectionsList
          inspections={inspections}
          establishments={establishments}
          inspectors={inspectors}
        />
      )}
    </div>
  );
}
