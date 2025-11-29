import React, { useEffect, useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { encounters, alerts } from '../../services/api';
import { Encounter, Vital, Alert, CopilotResponse, DischargePlan } from '../../types';
import {
    Activity, AlertTriangle, Brain, FileText, Thermometer, Heart, Wind
} from 'lucide-react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

const EncounterDetail = () => {
    const { id } = useParams<{ id: string }>();
    // const navigate = useNavigate(); // Unused
    const [encounter, setEncounter] = useState<Encounter | null>(null);
    const [vitals, setVitals] = useState<Vital[]>([]);
    const [encounterAlerts, setEncounterAlerts] = useState<Alert[]>([]);
    const [copilot, setCopilot] = useState<CopilotResponse | null>(null);
    const [dischargePlan, setDischargePlan] = useState<DischargePlan | null>(null);
    const [loading, setLoading] = useState(true);
    const [copilotLoading, setCopilotLoading] = useState(false);
    // const [selectedAlertId, setSelectedAlertId] = useState<string | null>(null); // Unused

    const fetchData = useCallback(async () => {
        if (!id) return;
        try {
            const [encRes, vitalsRes, alertsRes] = await Promise.all([
                encounters.getOverview(id),
                encounters.getVitals(id),
                encounters.getAlerts(id)
            ]);
            setEncounter(encRes.data);
            setVitals(vitalsRes.data);
            setEncounterAlerts(alertsRes.data);

            if (encRes.data.status === 'discharged') {
                const planRes = await encounters.getDischargePlan(id);
                setDischargePlan(planRes.data);
            }
        } catch (error) {
            console.error('Error fetching encounter data:', error);
        } finally {
            setLoading(false);
        }
    }, [id]);

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, [fetchData]);

    const handleCopilot = async (alertId?: string) => {
        if (!id) return;
        setCopilotLoading(true);
        try {
            let res;
            if (alertId) {
                res = await alerts.getExplanation(alertId);
                // setSelectedAlertId(alertId);
            } else {
                res = await encounters.getCopilot(id);
                // setSelectedAlertId(null);
            }
            setCopilot(res.data);
        } catch (error) {
            console.error('Error fetching copilot:', error);
        } finally {
            setCopilotLoading(false);
        }
    };

    const handleResolveAlert = async (alertId: string) => {
        try {
            await alerts.resolve(alertId);
            fetchData(); // Refresh alerts
        } catch (error) {
            console.error('Error resolving alert:', error);
        }
    };

    const handleDischarge = async () => {
        if (!id) return;
        if (!window.confirm('Are you sure you want to discharge this patient?')) return;
        try {
            await encounters.discharge(id);
            fetchData();
        } catch (error) {
            console.error('Error discharging patient:', error);
            alert('Failed to discharge patient');
        }
    };

    const handleAutoDischargeCheck = async () => {
        try {
            await encounters.autoDischargeCheck();
            alert('Auto discharge check triggered. Please refresh in a moment.');
            fetchData();
        } catch (error) {
            console.error('Error triggering auto discharge:', error);
        }
    };

    if (loading || !encounter) {
        return <div className="flex items-center justify-center h-full">Loading...</div>;
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex justify-between items-start">
                <div>
                    <h1 className="text-2xl font-bold text-gray-800">{encounter.patient_name}</h1>
                    <div className="flex items-center gap-4 mt-2 text-gray-600">
                        <span>{encounter.patient_age} yrs, {encounter.patient_gender}</span>
                        <span>•</span>
                        <span>Room {encounter.room_number} ({encounter.department})</span>
                        <span>•</span>
                        <span className={`px-2 py-0.5 rounded text-sm font-medium ${encounter.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
                            }`}>
                            {encounter.status.toUpperCase()}
                        </span>
                    </div>
                    <div className="mt-2 text-sm text-gray-500">
                        Admitted: {new Date(encounter.admission_time).toLocaleString()}
                        {encounter.discharge_time && ` • Discharged: ${new Date(encounter.discharge_time).toLocaleString()}`}
                    </div>
                </div>
                <div className="flex gap-2">
                    {encounter.status === 'active' && (
                        <>
                            <button
                                onClick={handleAutoDischargeCheck}
                                className="px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition font-medium"
                            >
                                Auto Check
                            </button>
                            <button
                                onClick={handleDischarge}
                                className="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition font-medium"
                            >
                                Discharge
                            </button>
                        </>
                    )}
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column: Vitals & Alerts */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Vitals Chart */}
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                                <Activity className="w-5 h-5 text-blue-600" />
                                Vitals Trends
                            </h3>
                        </div>
                        <div className="h-64 w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <LineChart data={vitals}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis
                                        dataKey="timestamp"
                                        tickFormatter={(time) => new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    />
                                    <YAxis />
                                    <Tooltip labelFormatter={(label) => new Date(label).toLocaleString()} />
                                    <Legend />
                                    <Line type="monotone" dataKey="heart_rate" stroke="#ef4444" name="HR (bpm)" dot={false} />
                                    <Line type="monotone" dataKey="spo2" stroke="#3b82f6" name="SpO2 (%)" dot={false} />
                                    <Line type="monotone" dataKey="bp_systolic" stroke="#10b981" name="Sys BP" dot={false} />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>
                        {/* Latest Vitals Cards */}
                        <div className="grid grid-cols-4 gap-4 mt-6">
                            {[
                                { label: 'Heart Rate', value: vitals[vitals.length - 1]?.heart_rate, unit: 'bpm', icon: Heart, color: 'text-red-500' },
                                { label: 'SpO2', value: vitals[vitals.length - 1]?.spo2, unit: '%', icon: Wind, color: 'text-blue-500' },
                                { label: 'BP', value: `${vitals[vitals.length - 1]?.bp_systolic}/${vitals[vitals.length - 1]?.bp_diastolic}`, unit: 'mmHg', icon: Activity, color: 'text-green-500' },
                                { label: 'Temp', value: vitals[vitals.length - 1]?.temperature, unit: '°C', icon: Thermometer, color: 'text-orange-500' },
                            ].map((item, idx) => (
                                <div key={idx} className="bg-gray-50 p-3 rounded-lg">
                                    <div className="flex items-center gap-2 mb-1">
                                        <item.icon className={`w-4 h-4 ${item.color}`} />
                                        <span className="text-xs text-gray-500">{item.label}</span>
                                    </div>
                                    <p className="text-lg font-bold text-gray-800">{item.value || '--'} <span className="text-xs font-normal text-gray-500">{item.unit}</span></p>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Alerts List */}
                    <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                        <div className="p-6 border-b border-gray-100">
                            <h3 className="font-semibold text-gray-800 flex items-center gap-2">
                                <AlertTriangle className="w-5 h-5 text-orange-500" />
                                Alerts
                            </h3>
                        </div>
                        <div className="divide-y divide-gray-100">
                            {encounterAlerts.map((alert) => (
                                <div key={alert.id} className={`p-4 ${alert.status === 'resolved' ? 'bg-gray-50 opacity-75' : 'bg-white'}`}>
                                    <div className="flex items-start justify-between">
                                        <div className="flex gap-3">
                                            <div className={`mt-1 w-2 h-2 rounded-full flex-shrink-0 ${alert.severity === 'critical' ? 'bg-red-500' :
                                                alert.severity === 'high' ? 'bg-orange-500' : 'bg-yellow-500'
                                                }`} />
                                            <div>
                                                <p className="font-medium text-gray-800">{alert.message}</p>
                                                <p className="text-xs text-gray-500 mt-1">
                                                    {new Date(alert.created_at).toLocaleString()} • {alert.type}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="flex gap-2">
                                            <button
                                                onClick={() => handleCopilot(alert.id)}
                                                className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
                                            >
                                                Explain with AI
                                            </button>
                                            {alert.status !== 'resolved' && (
                                                <button
                                                    onClick={() => handleResolveAlert(alert.id)}
                                                    className="text-sm text-green-600 hover:text-green-800 font-medium"
                                                >
                                                    Resolve
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                            {encounterAlerts.length === 0 && (
                                <div className="p-8 text-center text-gray-500">No alerts for this encounter.</div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Column: AI Copilot & Discharge Plan */}
                <div className="space-y-6">
                    {/* AI Copilot */}
                    <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                        <div className="p-6 border-b border-gray-100 bg-gradient-to-r from-indigo-50 to-white">
                            <div className="flex items-center justify-between">
                                <h3 className="font-semibold text-indigo-900 flex items-center gap-2">
                                    <Brain className="w-5 h-5 text-indigo-600" />
                                    AI Doctor Copilot
                                </h3>
                                <button
                                    onClick={() => handleCopilot()}
                                    className="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded hover:bg-indigo-200 transition"
                                >
                                    Analyze Status
                                </button>
                            </div>
                        </div>
                        <div className="p-6">
                            {copilotLoading ? (
                                <div className="flex items-center justify-center py-8">
                                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                                </div>
                            ) : copilot ? (
                                <div className="space-y-4">
                                    <div className={`p-3 rounded-lg ${copilot.risk_level === 'high' ? 'bg-red-50 border border-red-100' :
                                        copilot.risk_level === 'medium' ? 'bg-yellow-50 border border-yellow-100' :
                                            'bg-green-50 border border-green-100'
                                        }`}>
                                        <p className="font-semibold text-sm capitalize mb-1">Risk Level: {copilot.risk_level}</p>
                                        <p className="text-sm text-gray-700">{copilot.summary}</p>
                                    </div>

                                    <div>
                                        <p className="text-sm font-semibold text-gray-700 mb-2">Suggested Checks:</p>
                                        <ul className="space-y-1">
                                            {copilot.suggested_checks.map((check, i) => (
                                                <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                                                    <span className="mt-1.5 w-1 h-1 bg-indigo-400 rounded-full flex-shrink-0"></span>
                                                    {check}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>

                                    <div>
                                        <p className="text-sm font-semibold text-gray-700 mb-2">Suggested Actions:</p>
                                        <ul className="space-y-1">
                                            {copilot.suggested_actions.map((action, i) => (
                                                <li key={i} className="text-sm text-gray-600 flex items-start gap-2">
                                                    <span className="mt-1.5 w-1 h-1 bg-indigo-400 rounded-full flex-shrink-0"></span>
                                                    {action}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                    <p className="text-xs text-gray-400 italic mt-4 border-t pt-2">
                                        AI generated suggestions. Please review manually.
                                    </p>
                                </div>
                            ) : (
                                <div className="text-center py-8 text-gray-500 text-sm">
                                    Select an alert or click "Analyze Status" to get AI insights.
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Discharge Plan (if discharged) */}
                    {dischargePlan && (
                        <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                            <div className="p-6 border-b border-gray-100 bg-green-50">
                                <h3 className="font-semibold text-green-900 flex items-center gap-2">
                                    <FileText className="w-5 h-5 text-green-600" />
                                    Discharge Plan
                                </h3>
                            </div>
                            <div className="p-6 space-y-4">
                                <p className="text-sm text-gray-700">{dischargePlan.summary}</p>

                                <div>
                                    <p className="text-sm font-semibold text-gray-700 mb-2">Home Care:</p>
                                    <ul className="list-disc list-inside text-sm text-gray-600">
                                        {dischargePlan.home_care_instructions.map((inst, i) => (
                                            <li key={i}>{inst}</li>
                                        ))}
                                    </ul>
                                </div>

                                <div>
                                    <p className="text-sm font-semibold text-gray-700 mb-2">Medications:</p>
                                    <ul className="list-disc list-inside text-sm text-gray-600">
                                        {dischargePlan.medications.map((med, i) => (
                                            <li key={i}>{med}</li>
                                        ))}
                                    </ul>
                                </div>

                                <div className="bg-blue-50 p-3 rounded-lg text-sm text-blue-800">
                                    Follow up in {dischargePlan.follow_up_days} days
                                    {dischargePlan.follow_up_date && ` (${new Date(dischargePlan.follow_up_date).toLocaleDateString()})`}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default EncounterDetail;
