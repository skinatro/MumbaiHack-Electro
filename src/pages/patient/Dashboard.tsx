import React, { useEffect, useState } from 'react';
import { patient } from '../../services/api';
import { Encounter, Vital, Alert, DischargePlan } from '../../types';
import {
    Activity, AlertTriangle, FileText, Heart, Thermometer,
    Wind, Home, Calendar, Phone
} from 'lucide-react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts";

const PatientDashboard = () => {
    const [encounter, setEncounter] = useState<Encounter | null>(null);
    const [vitals, setVitals] = useState<Vital[]>([]);
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [dischargePlan, setDischargePlan] = useState<DischargePlan | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Try to fetch active encounter first
                try {
                    const encRes = await patient.getEncounter();
                    setEncounter(encRes.data);

                    if (encRes.data.status === 'active') {
                        const [vitalsRes, alertsRes] = await Promise.all([
                            patient.getVitals(),
                            patient.getAlerts()
                        ]);
                        setVitals(vitalsRes.data);
                        setAlerts(alertsRes.data);
                    } else {
                        // If discharged, fetch post-discharge plan
                        const planRes = await patient.getPostDischarge();
                        setDischargePlan(planRes.data);
                    }
                } catch (err) {
                    // If no encounter found or error, maybe check for post-discharge directly if not active
                    // But usually getEncounter returns the latest one.
                    console.log("No active encounter or error fetching it", err);
                }
            } catch (error) {
                console.error('Error fetching patient data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return <div className="flex items-center justify-center h-full">Loading...</div>;
    }

    if (!encounter) {
        return (
            <div className="text-center py-12">
                <Home className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h2 className="text-xl font-semibold text-gray-800">Welcome to MumbaiHack Hospital</h2>
                <p className="text-gray-600 mt-2">You currently have no active records.</p>
            </div>
        );
    }

    // Active Encounter View
    if (encounter.status === 'active') {
        return (
            <div className="space-y-6">
                {/* Status Card */}
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between">
                        <div>
                            <h2 className="text-xl font-bold text-gray-800">Current Stay</h2>
                            <p className="text-gray-600 mt-1">
                                Room {encounter.room_number} • {encounter.department}
                            </p>
                        </div>
                        <div className={`px-4 py-2 rounded-full text-sm font-bold ${encounter.risk_level === 'critical' ? 'bg-red-100 text-red-700' :
                                encounter.risk_level === 'watch' ? 'bg-yellow-100 text-yellow-700' :
                                    'bg-green-100 text-green-700'
                            }`}>
                            Status: {encounter.risk_level?.toUpperCase() || 'STABLE'}
                        </div>
                    </div>
                </div>

                {/* Vitals Overview */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {[
                        { label: 'Heart Rate', value: vitals[vitals.length - 1]?.heart_rate, unit: 'bpm', icon: Heart, color: 'text-red-500' },
                        { label: 'SpO2', value: vitals[vitals.length - 1]?.spo2, unit: '%', icon: Wind, color: 'text-blue-500' },
                        { label: 'BP', value: `${vitals[vitals.length - 1]?.bp_systolic}/${vitals[vitals.length - 1]?.bp_diastolic}`, unit: 'mmHg', icon: Activity, color: 'text-green-500' },
                        { label: 'Temp', value: vitals[vitals.length - 1]?.temperature, unit: '°C', icon: Thermometer, color: 'text-orange-500' },
                    ].map((item, idx) => (
                        <div key={idx} className="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
                            <div className="flex items-center gap-2 mb-2">
                                <item.icon className={`w-5 h-5 ${item.color}`} />
                                <span className="text-sm text-gray-500">{item.label}</span>
                            </div>
                            <p className="text-2xl font-bold text-gray-800">
                                {item.value || '--'} <span className="text-sm font-normal text-gray-500">{item.unit}</span>
                            </p>
                        </div>
                    ))}
                </div>

                {/* Vitals Chart (Simplified) */}
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <h3 className="font-semibold text-gray-800 mb-4">Your Vitals History</h3>
                    <div className="h-48 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={vitals}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="timestamp" hide />
                                <YAxis />
                                <Tooltip labelFormatter={(label) => new Date(label).toLocaleTimeString()} />
                                <Line type="monotone" dataKey="heart_rate" stroke="#ef4444" dot={false} strokeWidth={2} />
                                <Line type="monotone" dataKey="spo2" stroke="#3b82f6" dot={false} strokeWidth={2} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Alerts (Patient Friendly) */}
                {alerts.length > 0 && (
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                        <h3 className="font-semibold text-gray-800 mb-4">Notifications</h3>
                        <div className="space-y-3">
                            {alerts.map((alert) => (
                                <div key={alert.id} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                                    <AlertTriangle className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                                    <div>
                                        <p className="text-sm text-blue-900">{alert.message}</p>
                                        <p className="text-xs text-blue-600 mt-1">
                                            {new Date(alert.created_at).toLocaleTimeString()}
                                        </p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        );
    }

    // Discharged View
    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <div className="bg-green-50 p-8 rounded-2xl text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CheckCircle className="w-8 h-8 text-green-600" />
                </div>
                <h2 className="text-2xl font-bold text-green-900">You have been discharged!</h2>
                <p className="text-green-700 mt-2">
                    We hope you are feeling better. Here is your recovery plan.
                </p>
            </div>

            {dischargePlan && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                    <div className="p-6 border-b border-gray-100">
                        <h3 className="font-bold text-gray-800 flex items-center gap-2">
                            <FileText className="w-5 h-5 text-indigo-600" />
                            Your Recovery Plan
                        </h3>
                    </div>
                    <div className="p-6 space-y-6">
                        <div>
                            <p className="text-sm font-semibold text-gray-700 mb-2">Summary</p>
                            <p className="text-gray-600 bg-gray-50 p-3 rounded-lg">{dischargePlan.summary}</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <p className="text-sm font-semibold text-gray-700 mb-2">Medications</p>
                                <ul className="space-y-2">
                                    {dischargePlan.medications.map((med, i) => (
                                        <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                                            <span className="mt-1.5 w-1.5 h-1.5 bg-green-500 rounded-full flex-shrink-0"></span>
                                            {med}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div>
                                <p className="text-sm font-semibold text-gray-700 mb-2">Home Care</p>
                                <ul className="space-y-2">
                                    {dischargePlan.home_care_instructions.map((inst, i) => (
                                        <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                                            <span className="mt-1.5 w-1.5 h-1.5 bg-blue-500 rounded-full flex-shrink-0"></span>
                                            {inst}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>

                        <div className="bg-indigo-50 p-4 rounded-lg flex items-center gap-4">
                            <Calendar className="w-6 h-6 text-indigo-600" />
                            <div>
                                <p className="font-semibold text-indigo-900">Follow-up Appointment</p>
                                <p className="text-sm text-indigo-700">
                                    In {dischargePlan.follow_up_days} days
                                    {dischargePlan.follow_up_date && ` • ${new Date(dischargePlan.follow_up_date).toLocaleDateString()}`}
                                </p>
                            </div>
                        </div>

                        <div className="border-t pt-4">
                            <p className="text-sm font-semibold text-gray-700 mb-2">Emergency Contact</p>
                            <div className="flex items-center gap-2 text-gray-600">
                                <Phone className="w-4 h-4" />
                                <span>If symptoms worsen, please call <strong>102</strong> or visit the nearest emergency room.</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

// Helper icon
import { CheckCircle } from 'lucide-react';

export default PatientDashboard;
