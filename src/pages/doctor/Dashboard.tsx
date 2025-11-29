import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { doctor } from '../../services/api';
import { Encounter, Alert } from '../../types';
import {
    User, AlertTriangle, Clock, ArrowRight
} from 'lucide-react';

const DoctorDashboard = () => {
    const navigate = useNavigate();
    const [encounters, setEncounters] = useState<Encounter[]>([]);
    const [recentAlerts, setRecentAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [patientsRes, alertsRes] = await Promise.all([
                    doctor.getPatients(),
                    doctor.getRecentAlerts()
                ]);
                setEncounters(patientsRes.data);
                setRecentAlerts(alertsRes.data);
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        // Poll every 30 seconds
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return <div className="flex items-center justify-center h-full">Loading...</div>;
    }

    const getRiskColor = (level?: string) => {
        switch (level) {
            case 'critical': return 'bg-red-100 text-red-700';
            case 'watch': return 'bg-yellow-100 text-yellow-700';
            default: return 'bg-green-100 text-green-700';
        }
    };

    return (
        <div className="space-y-6">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Active Patients</p>
                            <p className="text-2xl font-bold text-gray-800">{encounters.length}</p>
                        </div>
                        <div className="p-3 bg-blue-50 rounded-full">
                            <User className="w-6 h-6 text-blue-600" />
                        </div>
                    </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Critical Alerts</p>
                            <p className="text-2xl font-bold text-gray-800">
                                {recentAlerts.filter(a => a.severity === 'critical' || a.severity === 'high').length}
                            </p>
                        </div>
                        <div className="p-3 bg-red-50 rounded-full">
                            <AlertTriangle className="w-6 h-6 text-red-600" />
                        </div>
                    </div>
                </div>
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Avg Stay Duration</p>
                            <p className="text-2xl font-bold text-gray-800">3 Days</p>
                        </div>
                        <div className="p-3 bg-green-50 rounded-full">
                            <Clock className="w-6 h-6 text-green-600" />
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Active Encounters List */}
                <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                    <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                        <h3 className="font-semibold text-gray-800">Active Encounters</h3>
                    </div>
                    <div className="divide-y divide-gray-100">
                        {encounters.map((encounter) => (
                            <div
                                key={encounter.id}
                                className="p-4 hover:bg-gray-50 cursor-pointer transition"
                                onClick={() => navigate(`/doctor/encounters/${encounter.id}`)}
                            >
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                                            <User className="w-5 h-5 text-gray-600" />
                                        </div>
                                        <div>
                                            <p className="font-medium text-gray-800">{encounter.patient_name}</p>
                                            <p className="text-sm text-gray-500">
                                                {encounter.patient_age}y • {encounter.patient_gender} • Room {encounter.room_number}
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskColor(encounter.risk_level)}`}>
                                            {encounter.risk_level || 'stable'}
                                        </span>
                                        <ArrowRight className="w-4 h-4 text-gray-400" />
                                    </div>
                                </div>
                            </div>
                        ))}
                        {encounters.length === 0 && (
                            <div className="p-8 text-center text-gray-500">
                                No active patients found.
                            </div>
                        )}
                    </div>
                </div>

                {/* Recent Alerts */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                    <div className="p-6 border-b border-gray-100">
                        <h3 className="font-semibold text-gray-800">Recent Alerts</h3>
                    </div>
                    <div className="divide-y divide-gray-100">
                        {recentAlerts.map((alert) => (
                            <div
                                key={alert.id}
                                className="p-4 hover:bg-gray-50 cursor-pointer"
                                onClick={() => navigate(`/doctor/encounters/${alert.encounter_id}`)}
                            >
                                <div className="flex gap-3">
                                    <AlertTriangle className={`w-5 h-5 flex-shrink-0 ${alert.severity === 'critical' ? 'text-red-500' :
                                        alert.severity === 'high' ? 'text-orange-500' : 'text-yellow-500'
                                        }`} />
                                    <div>
                                        <p className="text-sm font-medium text-gray-800">{alert.message}</p>
                                        <p className="text-xs text-gray-500 mt-1">
                                            {alert.patient_name} • Room {alert.room_number}
                                        </p>
                                        <p className="text-xs text-gray-400 mt-1">
                                            {new Date(alert.created_at).toLocaleTimeString()}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                        {recentAlerts.length === 0 && (
                            <div className="p-8 text-center text-gray-500">
                                No recent alerts.
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DoctorDashboard;
