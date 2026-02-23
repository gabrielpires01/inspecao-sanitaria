import { useState } from 'react';
import { useSearchEstablishments } from './queries/useEstablishments';
import type { Establishment } from '@/lib/types';

interface UseEstablishmentSearchResult {
  search: string;
  setSearch: (value: string) => void;
  establishments: Establishment[];
  selected: Establishment | null;
  setSelected: (establishment: Establishment) => void;
  onClear: () => void;
  searching: boolean;
  error: string;
}

export function useEstablishmentSearch(): UseEstablishmentSearchResult {
  const [search, setSearch] = useState('');
  const [selected, setSelectedState] = useState<Establishment | null>(null);

  const {
    data: establishments = [],
    isLoading: searching,
    error,
  } = useSearchEstablishments(search);

  const handleSelect = (establishment: Establishment) => {
    setSelectedState(establishment);
    setSearch(establishment.name);
  };

  const handleClear = () => {
    setSelectedState(null);
    setSearch('');
  };

  return {
    search,
    setSearch,
    establishments,
    selected,
    setSelected: handleSelect,
    onClear: handleClear,
    searching,
    error: error?.message || '',
  };
}
