import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { inspectionsApi } from '@/lib/api';
import type { Inspection, InspectionCreate, FinalizeInspection } from '@/lib/types';

export const inspectionKeys = {
  all: ['inspections'] as const,
  lists: () => [...inspectionKeys.all, 'list'] as const,
  list: (filters: string) => [...inspectionKeys.lists(), { filters }] as const,
  details: () => [...inspectionKeys.all, 'detail'] as const,
  detail: (id: number) => [...inspectionKeys.details(), id] as const,
};

export function useInspections() {
  return useQuery({
    queryKey: inspectionKeys.lists(),
    queryFn: () => inspectionsApi.getAll(),
  });
}

export function useInspection(id: number) {
  return useQuery({
    queryKey: inspectionKeys.detail(id),
    queryFn: () => inspectionsApi.getById(id),
    enabled: !!id,
  });
}

export function useCreateInspection() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: InspectionCreate) => inspectionsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: inspectionKeys.lists() });
    },
  });
}

export function useFinalizeInspection() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: FinalizeInspection) => inspectionsApi.finalize(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: inspectionKeys.detail(variables.inspection_id),
      });
      queryClient.invalidateQueries({ queryKey: inspectionKeys.lists() });
    },
  });
}
