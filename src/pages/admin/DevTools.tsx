import React, { useState } from 'react';
import { encounters } from '../../services/api';
import { Play, Terminal } from 'lucide-react';

const DevTools = () => {
    const [output, setOutput] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const runAutoDischarge = async () => {
        setLoading(true);
        try {
            const response = await encounters.autoDischargeCheck();
            setOutput(response.data);
        } catch (error: any) {
            setOutput({ error: error.message, details: error.response?.data });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div className="bg-gray-900 text-gray-100 rounded-lg shadow-xl overflow-hidden">
                <div className="p-4 border-b border-gray-800 flex items-center gap-2">
                    <Terminal className="w-5 h-5 text-green-400" />
                    <h2 className="font-mono font-bold">Developer Console</h2>
                </div>

                <div className="p-6 space-y-6">
                    <div>
                        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Actions</h3>
                        <div className="flex gap-4">
                            <button
                                onClick={runAutoDischarge}
                                disabled={loading}
                                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded text-white font-mono text-sm flex items-center gap-2 transition disabled:opacity-50"
                            >
                                <Play className="w-4 h-4" />
                                {loading ? 'Running...' : 'Run Auto-Discharge Job'}
                            </button>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Output</h3>
                        <div className="bg-black rounded p-4 font-mono text-xs h-64 overflow-y-auto border border-gray-800">
                            {output ? (
                                <pre className="text-green-400 whitespace-pre-wrap">
                                    {JSON.stringify(output, null, 2)}
                                </pre>
                            ) : (
                                <span className="text-gray-600">// Waiting for command...</span>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DevTools;
