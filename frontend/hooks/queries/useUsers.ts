import { useQuery } from '@tanstack/react-query';
import { usersApi } from '@/lib/api';
import type { User } from '@/lib/types';

export const userKeys = {
  all: ['users'] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: number) => [...userKeys.details(), id] as const,
  multiple: (ids: number[]) => [...userKeys.details(), 'multiple', ids.sort()] as const,
};

export function useUser(id: number) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => usersApi.getById(id),
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
  });
}

export function useUsers(ids: number[]) {
  const sortedIds = [...ids].sort();
  return useQuery({
    queryKey: userKeys.multiple(sortedIds),
    queryFn: async () => {
      const results = await Promise.all(
        ids.map((id) => usersApi.getById(id).catch(() => null))
      );
      const map: Record<number, User> = {};
      results.forEach((user, index) => {
        if (user) {
          map[ids[index]] = user;
        }
      });
      return map;
    },
    enabled: ids.length > 0,
    staleTime: 5 * 60 * 1000,
  });
}
