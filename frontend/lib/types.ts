// Enums
export enum Status {
  clear = 1,
  has_irregularities = 2,
  immediate_prohibition = 3,
  finalized = 4,
  finalized_prohibition = 5,
  finalized_partial_prohibition = 6,
}

export enum Severity {
  low = 1,
  moderate = 2,
  major = 3,
  critical = 4,
  resolved = 5,
}

export enum FinalizeStatus {
  accordingly = 1,
  with_problems = 2,
  partial_prohibition = 3,
  prohibition = 4,
}

// Types
export interface User {
  id: number;
  username: string;
  full_name: string;
  email: string;
  role: number;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Establishment {
  id: number;
  name: string;
  address?: string;
  cep?: string;
  city?: string;
  created_at: string;
}

export interface Inspection {
  id: number;
  establishment_id: number;
  inspector_id: number;
  date_time?: string;
  status: Status;
  created_at: string;
}

export interface Irregularity {
  id: number;
  inspection_id: number;
  inspector_id: number;
  description: string;
  severity: Severity;
  requires_interruption: boolean;
  created_at: string;
}

export interface InspectionCreate {
  establishment_id: number;
  date_time?: string;
  status: Status;
}

export interface IrregularityCreate {
  inspection_id: number;
  description: string;
  severity: Severity;
  requires_interruption: boolean;
}

export interface FinalizeInspection {
  inspection_id: number;
  status: FinalizeStatus;
  pending_issues: string;
}
