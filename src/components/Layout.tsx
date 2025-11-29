import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
    Menu, X, User, LogOut, Home, Activity, Calendar,
    FileText, Bell, Settings, PlusCircle
} from 'lucide-react';

const Layout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [showProfile, setShowProfile] = useState(false);

    const doctorMenuItems = [
        { icon: Home, label: 'Dashboard', path: '/doctor/dashboard' },
        { icon: PlusCircle, label: 'Admit Patient', path: '/doctor/admit' },
    ];

    const patientMenuItems = [
        { icon: Home, label: 'Dashboard', path: '/patient/dashboard' },
    ];

    const menuItems = user?.role === 'doctor' ? doctorMenuItems : patientMenuItems;

    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <div className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-indigo-900 text-white transition-all duration-300 flex flex-col`}>
                <div className="p-4 flex items-center justify-between">
                    {sidebarOpen && <h1 className="text-xl font-bold">MumbaiHack</h1>}
                    <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 hover:bg-indigo-800 rounded">
                        {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                    </button>
                </div>

                <nav className="flex-1 px-2 py-2 space-y-2">
                    {menuItems.map((item, idx) => (
                        <button
                            key={idx}
                            onClick={() => navigate(item.path)}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${location.pathname === item.path ? 'bg-indigo-800 text-white' : 'hover:bg-indigo-800'
                                }`}
                        >
                            <item.icon className="w-5 h-5" />
                            {sidebarOpen && <span>{item.label}</span>}
                        </button>
                    ))}
                </nav>

                {/* Profile Section */}
                <div className="p-4 border-t border-indigo-800 relative">
                    <button
                        onClick={() => setShowProfile(!showProfile)}
                        className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-indigo-800 transition"
                    >
                        <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center">
                            <User className="w-5 h-5" />
                        </div>
                        {sidebarOpen && (
                            <div className="flex-1 text-left">
                                <p className="text-sm font-medium">{user?.name || 'User'}</p>
                                <p className="text-xs text-indigo-300 capitalize">{user?.role}</p>
                            </div>
                        )}
                    </button>

                    {showProfile && (
                        <div className="absolute bottom-full left-4 mb-2 bg-white text-gray-800 rounded-lg shadow-xl p-2 w-48">
                            <button
                                onClick={logout}
                                className="w-full flex items-center gap-2 px-4 py-2 hover:bg-gray-100 rounded text-red-600"
                            >
                                <LogOut className="w-4 h-4" />
                                <span>Logout</span>
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
                <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-800">
                            {user?.role === 'doctor' ? 'Doctor Dashboard' : 'Patient Portal'}
                        </h2>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                    <Outlet />
                </div>
            </div>
        </div>
    );
};

export default Layout;
