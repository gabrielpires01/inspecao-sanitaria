import React from 'react';
import type { Establishment } from '@/lib/types';
import styles from './EstablishmentSearch.module.css';

interface EstablishmentSearchProps {
  value: string;
  onChange: (value: string) => void;
  establishments: Establishment[];
  selected: Establishment | null;
  onSelect: (establishment: Establishment) => void;
  onClear: () => void;
  searching: boolean;
}

export default function EstablishmentSearch({
  value,
  onChange,
  establishments,
  selected,
  onSelect,
  onClear,
  searching,
}: EstablishmentSearchProps) {
  return (
    <div className={styles.inputGroup}>
      <label htmlFor="establishment">Estabelecimento *</label>
      <input
        id="establishment"
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Digite o nome do estabelecimento..."
        required
        className={styles.input}
      />
      {searching && <div className={styles.searching}>Buscando...</div>}
      {establishments.length > 0 && !selected && (
        <div className={styles.dropdown}>
          {establishments.map((est) => (
            <div
              key={est.id}
              className={styles.dropdownItem}
              onClick={() => onSelect(est)}
            >
              <div className={styles.name}>{est.name}</div>
              {est.address && (
                <div className={styles.address}>{est.address}</div>
              )}
              {est.city && <div className={styles.city}>{est.city}</div>}
            </div>
          ))}
        </div>
      )}
      {selected && (
        <div className={styles.selected}>
          <strong>Selecionado:</strong> {selected.name}
          <button
            type="button"
            onClick={onClear}
            className={styles.clearButton}
          >
            Limpar
          </button>
        </div>
      )}
    </div>
  );
}
