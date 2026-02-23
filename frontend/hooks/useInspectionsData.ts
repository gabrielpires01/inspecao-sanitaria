import { useMemo } from 'react';
import { useInspections } from './queries/useInspections';
import { useEstablishments } from './queries/useEstablishments';
import { useUsers } from './queries/useUsers';

export function useInspectionsData() {
  const { data: inspections = [], loading, error } = useInspections();

  const establishmentIds = useMemo(() => {
    const ids = new Set<number>();
    inspections.forEach((inspection) => {
      ids.add(inspection.establishment_id);
    });
    return Array.from(ids);
  }, [inspections]);

  const inspectorIds = useMemo(() => {
    const ids = new Set<number>();
    inspections.forEach((inspection) => {
      ids.add(inspection.inspector_id);
    });
    return Array.from(ids);
  }, [inspections]);

  const {
    data: establishments = {},
    isLoading: loadingEstablishments,
  } = useEstablishments(establishmentIds);

  const {
    data: inspectors = {},
    isLoading: loadingInspectors,
  } = useUsers(inspectorIds);

  return {
    inspections,
    establishments,
    inspectors,
    loading: loading || loadingEstablishments || loadingInspectors,
    error: error?.message || '',
    reload: () => {},
  };
}
