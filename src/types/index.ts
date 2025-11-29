export interface User {
    id: string;
    name: string;
    email: string;
    role: 'doctor' | 'patient' | 'admin';
}

export interface AuthResponse {
    access_token: string;
    user: User;
}

export interface Patient {
    id: string;
    name: string;
    age: number;
    gender: string;
}

export interface Vital {
    id: string;
    encounter_id: string;
    heart_rate: number;
    spo2: number;
    respiratory_rate: number;
    bp_systolic: number;
    bp_diastolic: number;
    temperature: number;
    timestamp: string;
}

export interface Alert {
    id: string;
    encounter_id: string;
    patient_name?: string; // Added for convenience in lists
    room_number?: string; // Added for convenience in lists
    type: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    message: string;
    created_at: string;
    status: 'new' | 'acknowledged' | 'resolved';
}

export interface Encounter {
    id: string;
    patient_id: string;
    patient_name: string;
    patient_age: number;
    patient_gender: string;
    room_number: string;
    department: string;
    status: 'active' | 'discharged';
    admission_time: string;
    discharge_time?: string;
    risk_level?: 'stable' | 'watch' | 'critical';
}

export interface DischargePlan {
    summary: string;
    home_care_instructions: string[];
    medications: string[];
    follow_up_days: number;
    follow_up_date?: string;
}

export interface CopilotResponse {
    summary: string;
    risk_level: 'low' | 'medium' | 'high';
    suggested_checks: string[];
    suggested_actions: string[];
}

export interface AdmissionRequest {
    patient_name: string;
    age: number;
    gender: string;
    symptoms: string[];
    complaint: string;
    severity_hint: 'low' | 'medium' | 'high';
    department?: string;
}

export interface AdmissionResponse {
    patient_id: string;
    encounter_id: string;
    room_number: string;
    department: string;
    triage_decision: string;
    notes: string;
}

export interface LLMHealth {
    status: string;
    model: string;
    message?: string;
    error?: string;
}
