import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { irregularitiesApi } from '@/lib/api';
import type { Irregularity, IrregularityCreate } from '@/lib/types';
import { inspectionKeys } from './useInspections';

export const irregularityKeys = {
  all: ['irregularities'] as const,
  lists: () => [...irregularityKeys.all, 'list'] as const,
  byInspection: (inspectionId: number) =>
    [...irregularityKeys.lists(), 'inspection', inspectionId] as const,
};

export function useIrregularitiesByInspection(inspectionId: number) {
  return useQuery({
    queryKey: irregularityKeys.byInspection(inspectionId),
    queryFn: () => irregularitiesApi.getByInspection(inspectionId),
    enabled: !!inspectionId,
  });
}

export function useCreateIrregularity() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: IrregularityCreate) => irregularitiesApi.create(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: irregularityKeys.byInspection(variables.inspection_id),
      });
      queryClient.invalidateQueries({
        queryKey: inspectionKeys.detail(variables.inspection_id),
      });
      queryClient.invalidateQueries({ queryKey: inspectionKeys.lists() });
    },
  });
}
