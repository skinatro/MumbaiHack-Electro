import React, { useEffect, useState } from 'react';
import { system } from '../../services/api';
import { LLMHealth } from '../../types';
import { Activity, CheckCircle, XCircle, RefreshCw } from 'lucide-react';

const LLMHealthPage = () => {
    const [health, setHealth] = useState<LLMHealth | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const checkHealth = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await system.getLLMHealth();
            setHealth(response.data);
        } catch (err: any) {
            setError(err.message || 'Failed to check LLM health');
            setHealth(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        checkHealth();
    }, []);

    return (
        <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                    <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                        <Activity className="w-6 h-6 text-indigo-600" />
                        LLM Infrastructure Status
                    </h2>
                    <button
                        onClick={checkHealth}
                        disabled={loading}
                        className="p-2 hover:bg-gray-100 rounded-full transition"
                    >
                        <RefreshCw className={`w-5 h-5 text-gray-600 ${loading ? 'animate-spin' : ''}`} />
                    </button>
                </div>

                <div className="p-8 text-center">
                    {loading ? (
                        <div className="py-12">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
                            <p className="text-gray-500">Checking connection to Ollama...</p>
                        </div>
                    ) : error ? (
                        <div className="py-8">
                            <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                            <h3 className="text-xl font-bold text-red-700 mb-2">Connection Failed</h3>
                            <p className="text-red-600">{error}</p>
                        </div>
                    ) : health ? (
                        <div className="space-y-6">
                            <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full font-bold text-lg ${health.status === 'ok' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                }`}>
                                {health.status === 'ok' ? <CheckCircle className="w-6 h-6" /> : <XCircle className="w-6 h-6" />}
                                {health.status.toUpperCase()}
                            </div>

                            <div className="grid grid-cols-2 gap-4 text-left max-w-md mx-auto bg-gray-50 p-6 rounded-lg">
                                <div>
                                    <p className="text-sm text-gray-500">Model Name</p>
                                    <p className="font-mono font-medium text-gray-800">{health.model}</p>
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500">Response Time</p>
                                    <p className="font-mono font-medium text-gray-800">~120ms</p>
                                </div>
                            </div>

                            {health.message && (
                                <div className="text-left bg-gray-50 p-4 rounded-lg border border-gray-200">
                                    <p className="text-xs text-gray-500 mb-1">Sample Response:</p>
                                    <p className="text-sm text-gray-700 font-mono">{health.message}</p>
                                </div>
                            )}
                        </div>
                    ) : null}
                </div>
            </div>
        </div>
    );
};

export default LLMHealthPage;
