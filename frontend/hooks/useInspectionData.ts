import { useMemo } from 'react';
import { useInspection } from './queries/useInspections';
import { useEstablishment } from './queries/useEstablishments';
import { useUser, useUsers } from './queries/useUsers';
import { useIrregularitiesByInspection } from './queries/useIrregularities';

export function useInspectionData(inspectionId: number) {
  const {
    data: inspection,
    isLoading: loadingInspection,
    error: errorInspection,
  } = useInspection(inspectionId);

  const {
    data: irregularities = [],
    isLoading: loadingIrregularities,
  } = useIrregularitiesByInspection(inspectionId);

  const {
    data: establishment,
    isLoading: loadingEstablishment,
  } = useEstablishment(inspection?.establishment_id || 0);

  const {
    data: inspector,
    isLoading: loadingInspector,
  } = useUser(inspection?.inspector_id || 0);

  const inspectorIds = useMemo(() => {
    const ids = new Set<number>();
    irregularities.forEach((irr) => {
      if (irr.inspector_id) {
        ids.add(irr.inspector_id);
      }
    });
    return Array.from(ids);
  }, [irregularities]);

  const {
    data: irregularityInspectors = {},
    isLoading: loadingIrregularityInspectors,
  } = useUsers(inspectorIds);

  return {
    inspection: inspection || null,
    irregularities,
    establishment: establishment || null,
    inspector: inspector || null,
    irregularityInspectors,
    loading:
      loadingInspection ||
      loadingIrregularities ||
      loadingEstablishment ||
      loadingInspector ||
      loadingIrregularityInspectors,
    error: errorInspection?.message || '',
    reload: () => {},
  };
}
