import { useQuery } from '@tanstack/react-query';
import { establishmentsApi } from '@/lib/api';
import type { Establishment } from '@/lib/types';

export const establishmentKeys = {
  all: ['establishments'] as const,
  lists: () => [...establishmentKeys.all, 'list'] as const,
  search: (name: string) => [...establishmentKeys.lists(), 'search', name] as const,
  details: () => [...establishmentKeys.all, 'detail'] as const,
  detail: (id: number) => [...establishmentKeys.details(), id] as const,
};

export function useEstablishment(id: number) {
  return useQuery({
    queryKey: establishmentKeys.detail(id),
    queryFn: () => establishmentsApi.getById(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  });
}

export function useEstablishments(ids: number[]) {
  const sortedIds = [...ids].sort();
  return useQuery({
    queryKey: [...establishmentKeys.details(), 'multiple', sortedIds],
    queryFn: async () => {
      const results = await Promise.all(
        ids.map((id) =>
          establishmentsApi.getById(id).catch(() => null)
        )
      );
      const map: Record<number, Establishment> = {};
      results.forEach((est, index) => {
        if (est) {
          map[ids[index]] = est;
        }
      });
      return map;
    },
    enabled: ids.length > 0,
    staleTime: 5 * 60 * 1000,
  });
}

export function useSearchEstablishments(name: string) {
  return useQuery({
    queryKey: establishmentKeys.search(name),
    queryFn: () => establishmentsApi.search(name),
    enabled: name.length >= 2,
    staleTime: 30 * 1000,
  });
}
