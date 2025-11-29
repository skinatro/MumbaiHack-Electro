import axios from 'axios';
import {
    User, AuthResponse, Encounter, Alert, Vital, DischargePlan,
    CopilotResponse, AdmissionRequest, AdmissionResponse, LLMHealth
} from '../types';

const api = axios.create({
    baseURL: '/api', // We will configure Vite proxy to forward /api to the backend
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to attach the token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Add a response interceptor to handle 401s
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Clear token and redirect to login if unauthorized
            localStorage.removeItem('token');
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export const auth = {
    login: (credentials: { email: string; password: string }) => api.post<AuthResponse>('/auth/login', credentials),
    getMe: () => api.get<User>('/auth/me'),
};

export const doctor = {
    getPatients: () => api.get<Encounter[]>('/doctors/me/patients'),
    getRecentAlerts: () => api.get<Alert[]>('/doctors/me/alerts/recent'),
    admitPatient: (data: AdmissionRequest) => api.post<AdmissionResponse>('/admissions/auto', data),
};

export const patient = {
    getEncounter: () => api.get<Encounter>('/patients/me/encounter'),
    getVitals: () => api.get<Vital[]>('/patients/me/vitals/recent'),
    getAlerts: () => api.get<Alert[]>('/patients/me/alerts'),
    getPostDischarge: () => api.get<DischargePlan>('/patients/me/post_discharge'),
};

export const encounters = {
    getOverview: (id: string) => api.get<Encounter>(`/encounters/${id}/overview`),
    getVitals: (id: string) => api.get<Vital[]>(`/encounters/${id}/vitals`),
    getAlerts: (id: string) => api.get<Alert[]>(`/encounters/${id}/alerts`),
    getDischargePlan: (id: string) => api.get<DischargePlan>(`/encounters/${id}/discharge_plan`),
    discharge: (id: string) => api.patch(`/encounters/${id}/discharge`),
    autoDischargeCheck: () => api.post('/discharge/auto/run'),
    getCopilot: (id: string) => api.get<CopilotResponse>(`/encounters/${id}/copilot`),
};

export const alerts = {
    resolve: (id: string) => api.patch(`/alerts/${id}/resolve`),
    getExplanation: (id: string) => api.get<CopilotResponse>(`/alerts/${id}/explanation`),
};

export const system = {
    getLLMHealth: () => api.get<LLMHealth>('/llm/health'),
};

export default api;
