import axios from 'axios';
import type {
  Token,
  User,
  Inspection,
  Irregularity,
  Establishment,
  InspectionCreate,
  IrregularityCreate,
  FinalizeInspection,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (username: string, password: string): Promise<Token> => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

export const establishmentsApi = {
  search: async (name: string): Promise<Establishment[]> => {
    const response = await api.get('/api/establishments/search', {
      params: { name },
    });
    return response.data;
  },

  getById: async (id: number): Promise<Establishment> => {
    const response = await api.get(`/api/establishments/${id}`);
    return response.data;
  },
};

export const inspectionsApi = {
  getAll: async (): Promise<Inspection[]> => {
    const response = await api.get('/api/inspections');
    return response.data;
  },

  getById: async (id: number): Promise<Inspection> => {
    const response = await api.get(`/api/inspections/${id}`);
    return response.data;
  },

  create: async (data: InspectionCreate): Promise<Inspection> => {
    const response = await api.post('/api/inspections', data);
    return response.data;
  },

  finalize: async (data: FinalizeInspection): Promise<any> => {
    const response = await api.post(
      `/api/inspections/finalize/${data.inspection_id}`,
      data
    );
    return response.data;
  },
};

export const irregularitiesApi = {
  getByInspection: async (inspectionId: number): Promise<Irregularity[]> => {
    const response = await api.get(`/api/irregularities/inspection/${inspectionId}`);
    return response.data;
  },

  create: async (data: IrregularityCreate): Promise<Irregularity> => {
    const response = await api.post('/api/irregularities', data);
    return response.data;
  },
};

export const usersApi = {
  getById: async (id: number): Promise<User> => {
    const response = await api.get(`/api/users/${id}`);
    return response.data;
  },
};
