import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { doctor } from '../../services/api';
import { AdmissionRequest } from '../../types';
import { UserPlus, Save } from 'lucide-react';

const Admission = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<AdmissionRequest>({
        patient_name: '',
        age: 0,
        gender: 'Male',
        symptoms: [],
        complaint: '',
        severity_hint: 'low',
        department: 'General'
    });
    const [symptomsInput, setSymptomsInput] = useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'age' ? parseInt(value) || 0 : value
        }));
    };

    const handleSymptomsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSymptomsInput(e.target.value);
    };

    const handleAddSymptom = () => {
        if (symptomsInput.trim()) {
            setFormData(prev => ({
                ...prev,
                symptoms: [...prev.symptoms, symptomsInput.trim()]
            }));
            setSymptomsInput('');
        }
    };

    const handleRemoveSymptom = (index: number) => {
        setFormData(prev => ({
            ...prev,
            symptoms: prev.symptoms.filter((_, i) => i !== index)
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await doctor.admitPatient(formData);
            alert(`Patient admitted successfully! Assigned to Room ${response.data.room_number}`);
            navigate(`/doctor/encounters/${response.data.encounter_id}`);
        } catch (error) {
            console.error('Error admitting patient:', error);
            alert('Failed to admit patient. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-3xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                <div className="p-6 border-b border-gray-100 bg-indigo-50">
                    <h2 className="text-xl font-bold text-indigo-900 flex items-center gap-2">
                        <UserPlus className="w-6 h-6 text-indigo-600" />
                        Admit New Patient
                    </h2>
                    <p className="text-sm text-indigo-600 mt-1">
                        Enter patient details for auto-triage and room assignment.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Patient Name</label>
                            <input
                                type="text"
                                name="patient_name"
                                value={formData.patient_name}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                required
                            />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
                                <input
                                    type="number"
                                    name="age"
                                    value={formData.age}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                    required
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                                <select
                                    name="gender"
                                    value={formData.gender}
                                    onChange={handleChange}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                >
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Primary Complaint</label>
                        <textarea
                            name="complaint"
                            value={formData.complaint}
                            onChange={handleChange}
                            rows={3}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            placeholder="Describe the patient's main complaint..."
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Symptoms</label>
                        <div className="flex gap-2 mb-2">
                            <input
                                type="text"
                                value={symptomsInput}
                                onChange={handleSymptomsChange}
                                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSymptom())}
                                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                                placeholder="Add a symptom (e.g., Fever, Cough)"
                            />
                            <button
                                type="button"
                                onClick={handleAddSymptom}
                                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
                            >
                                Add
                            </button>
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {formData.symptoms.map((symptom, index) => (
                                <span key={index} className="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-sm flex items-center gap-2">
                                    {symptom}
                                    <button
                                        type="button"
                                        onClick={() => handleRemoveSymptom(index)}
                                        className="hover:text-indigo-900"
                                    >
                                        &times;
                                    </button>
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Severity Hint</label>
                            <select
                                name="severity_hint"
                                value={formData.severity_hint}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Department</label>
                            <select
                                name="department"
                                value={formData.department}
                                onChange={handleChange}
                                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                            >
                                <option value="General">General</option>
                                <option value="ICU">ICU</option>
                                <option value="Emergency">Emergency</option>
                            </select>
                        </div>
                    </div>

                    <div className="pt-4 border-t border-gray-100 flex justify-end">
                        <button
                            type="submit"
                            disabled={loading}
                            className={`px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 transition flex items-center gap-2 ${loading ? 'opacity-70 cursor-not-allowed' : ''
                                }`}
                        >
                            <Save className="w-5 h-5" />
                            {loading ? 'Admitting...' : 'Admit Patient'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Admission;
