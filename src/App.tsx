'use client'
import React, { useState } from 'react';
import { User, Bell, LogOut, Send, Menu, X, Search, Plus, Activity, Calendar, FileText, Settings, Home, Clock, Download, Eye } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";


// Mock patient data
const PATIENTS_DATA = [
  { id: 1, name: "John Smith", age: 45, condition: "Hypertension", lastVisit: "2024-11-20", status: "Stable" },
  { id: 2, name: "Sarah Johnson", age: 32, condition: "Diabetes Type 2", lastVisit: "2024-11-22", status: "Monitoring" },
  { id: 3, name: "Michael Brown", age: 58, condition: "Heart Disease", lastVisit: "2024-11-25", status: "Critical" },
  { id: 4, name: "Emily Davis", age: 28, condition: "Asthma", lastVisit: "2024-11-18", status: "Stable" },
  { id: 5, name: "Robert Wilson", age: 65, condition: "Arthritis", lastVisit: "2024-11-21", status: "Stable" },
];

// Mock appointments data
const APPOINTMENTS_DATA = [
  { id: 1, doctor: "Dr. Sarah Williams", specialty: "Cardiologist", patient: "John Smith", time: "09:00 AM", date: "2024-11-28", status: "Confirmed" },
  { id: 2, doctor: "Dr. Michael Chen", specialty: "Endocrinologist", patient: "Sarah Johnson", time: "10:30 AM", date: "2024-11-28", status: "Confirmed" },
  { id: 3, doctor: "Dr. Sarah Williams", specialty: "Cardiologist", patient: "Michael Brown", time: "11:00 AM", date: "2024-11-28", status: "Pending" },
  { id: 4, doctor: "Dr. Emily Rodriguez", specialty: "Pulmonologist", patient: "Emily Davis", time: "02:00 PM", date: "2024-11-28", status: "Confirmed" },
  { id: 5, doctor: "Dr. James Patterson", specialty: "Rheumatologist", patient: "Robert Wilson", time: "03:30 PM", date: "2024-11-28", status: "Confirmed" },
  { id: 6, doctor: "Dr. Michael Chen", specialty: "Endocrinologist", patient: "John Smith", time: "09:30 AM", date: "2024-11-29", status: "Pending" },
];

const MEDICAL_REPORTS = [
  {
    id: 1,
    title: "Blood Test Report",
    date: "2024-11-20",
    doctor: "Dr. Sarah Williams",
    type: "Lab Report",
    status: "Completed",
    findings: "All parameters within normal range. Hemoglobin: 14.2 g/dL, WBC: 7,500/mcL",
    fileSize: "245 KB"
  },
  {
    id: 2,
    title: "ECG Report",
    date: "2024-11-15",
    doctor: "Dr. Sarah Williams",
    type: "Diagnostic",
    status: "Completed",
    findings: "Normal sinus rhythm. Heart rate: 72 bpm. No abnormalities detected.",
    fileSize: "180 KB"
  },
  {
    id: 3,
    title: "Chest X-Ray",
    date: "2024-11-10",
    doctor: "Dr. Emily Rodriguez",
    type: "Imaging",
    status: "Completed",
    findings: "Clear lung fields. No evidence of infection or abnormality. Heart size normal.",
    fileSize: "1.2 MB"
  },
  {
    id: 4,
    title: "Diabetes Panel",
    date: "2024-11-05",
    doctor: "Dr. Michael Chen",
    type: "Lab Report",
    status: "Completed",
    findings: "HbA1c: 5.8%, Fasting glucose: 95 mg/dL. Well controlled.",
    fileSize: "198 KB"
  },
  {
    id: 5,
    title: "Lipid Profile",
    date: "2024-10-28",
    doctor: "Dr. Sarah Williams",
    type: "Lab Report",
    status: "Completed",
    findings: "Total Cholesterol: 185 mg/dL, LDL: 110 mg/dL, HDL: 55 mg/dL, Triglycerides: 100 mg/dL",
    fileSize: "210 KB"
  },
  {
    id: 6,
    title: "Thyroid Function Test",
    date: "2024-10-15",
    doctor: "Dr. Michael Chen",
    type: "Lab Report",
    status: "Pending",
    findings: "Results awaiting final review by physician.",
    fileSize: "156 KB"
  }
];

// Login Component
const LoginPage = ({ onLogin }) => {
  const [userType, setUserType] = useState('doctor');
  const [credentials, setCredentials] = useState({ email: '', password: '' });


  const handleSubmit = () => {
    onLogin(userType);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-indigo-600 rounded-full mb-4">
            <Activity className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800">Healthcare AI</h1>
          <p className="text-gray-600 mt-2">Sign in to your account</p>
        </div>

        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">I am a</label>
            <div className="grid grid-cols-2 gap-4">
              <button
                type="button"
                onClick={() => setUserType('doctor')}
                className={`py-3 px-4 rounded-lg font-medium transition ${
                  userType === 'doctor'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Doctor
              </button>
              <button
                type="button"
                onClick={() => setUserType('patient')}
                className={`py-3 px-4 rounded-lg font-medium transition ${
                  userType === 'patient'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Patient
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={credentials.email}
              onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="your@email.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={credentials.password}
              onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            onClick={handleSubmit}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg font-medium hover:bg-indigo-700 transition"
          >
            Sign In
          </button>
        </div>

        <p className="text-center text-sm text-gray-600 mt-6">
          Don't have an account? <a href="#" className="text-indigo-600 hover:underline">Sign up</a>
        </p>
      </div>
    </div>
  );
};

function AppointmentForm({ setActivePage }) {
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    problem: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Appointment Booked Successfully!");
    console.log(formData);
    setActivePage("dashboard"); 
  };

  return (
    <div className="max-w-lg mx-auto bg-white shadow-lg rounded-lg p-6 space-y-6">

      <h2 className="text-2xl font-bold text-gray-800 text-center">
        Book Appointment
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">

        <div>
          <label className="block text-gray-700 mb-1">Patient Name</label>
          <input
            type="text"
            name="name"
            required
            value={formData.name}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
            placeholder="Enter your name"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-1">Age</label>
          <input
            type="number"
            name="age"
            required
            value={formData.age}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
            placeholder="Enter your age"
          />
        </div>

        <div>
          <label className="block text-gray-700 mb-1">Problem Facing</label>
          <textarea
            name="problem"
            required
            value={formData.problem}
            onChange={handleChange}
            className="w-full p-2 border rounded-md"
            rows="3"
            placeholder="Describe your problem"
          ></textarea>
        </div>

        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700"
        >
          Submit
        </button>

        <button
          type="button"
          onClick={() => setActivePage("dashboard")}
          className="w-full bg-gray-300 text-black py-2 rounded-md hover:bg-gray-400 mt-2"
        >
          Cancel
        </button>

      </form>
    </div>
  );
}


// Chatbot Component
const Chatbot = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI healthcare assistant. How can I help you today?", sender: 'ai' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;

    const newMessage = { id: Date.now(), text: input, sender: 'user' };
    setMessages([...messages, newMessage]);
    setInput('');

    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        text: "I'm processing your request. As an AI assistant, I can help with patient information, medical queries, and administrative tasks.",
        sender: 'ai'
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      <div className="bg-indigo-600 text-white p-4 rounded-t-lg">
        <h2 className="text-lg font-semibold">AI Assistant</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
              msg.sender === 'user' 
                ? 'bg-indigo-600 text-white' 
                : 'bg-gray-100 text-gray-800'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
          <button
            onClick={handleSend}
            className="bg-indigo-600 text-white p-2 rounded-lg hover:bg-indigo-700 transition"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

// Main Dashboard Component
const Dashboard = ({ userType, onLogout }) => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activePage, setActivePage] = useState('dashboard');
  const [appointmentFilter, setAppointmentFilter] = useState('all');
const [reportFilter, setReportFilter] = useState('all');

  const notifications = [
    { id: 1, text: "New patient registered", time: "5 min ago" },
    { id: 2, text: "Lab results available", time: "1 hour ago" },
    { id: 3, text: "Appointment reminder", time: "2 hours ago" },
  ];

  const filteredPatients = PATIENTS_DATA.filter(patient =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const menuItems = userType === 'doctor' ? [
    { icon: Home, label: 'Dashboard', path: 'dashboard' },
    { icon: User, label: 'Patients', path: 'patients' },
    { icon: Calendar, label: 'Appointments', path: 'appointments' },

  ] : [
    { icon: Home, label: 'Dashboard', path: 'dashboard' },
    { icon: Activity, label: 'Form', path: 'form' },
    { icon: Calendar, label: 'Appointments History', path: 'appointments' },
    { icon: FileText, label: 'Medical Records', path: 'records' },
  ];

  const [mode, setMode] = useState("week");

const weeklyData = [
  { label: "Mon", new: 5, followUp: 12 },
  { label: "Tue", new: 8, followUp: 15 },
  { label: "Wed", new: 6, followUp: 10 },
  { label: "Thu", new: 9, followUp: 18 },
  { label: "Fri", new: 4, followUp: 11 },
  { label: "Sat", new: 3, followUp: 6 },
  { label: "Sun", new: 2, followUp: 4 },
];

const monthlyData = [
  { label: "Week 1", new: 40, followUp: 90 },
  { label: "Week 2", new: 50, followUp: 110 },
  { label: "Week 3", new: 45, followUp: 100 },
  { label: "Week 4", new: 35, followUp: 85 },
];

const displayData = mode === "week" ? weeklyData : monthlyData;


  return (
    <div className="flex h-screen bg-gray-50">
      {/* Left Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-indigo-900 text-white transition-all duration-300 flex flex-col`}>
        <div className="p-4 flex items-center justify-between">
          {sidebarOpen && <h1 className="text-xl font-bold">HealthCare AI</h1>}
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 hover:bg-indigo-800 rounded">
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        <nav className="flex-1 px-2 py-2 space-y-2">
          {menuItems.map((item, idx) => (
            <button
              key={idx}
              onClick={() => setActivePage(item.path)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition ${
                activePage === item.path ? 'bg-indigo-800 text-white' : 'hover:bg-indigo-800'
              }`}
            >
              <item.icon className="w-5 h-5" />
              {sidebarOpen && <span>{item.label}</span>}
            </button>
          ))}
        </nav>

        {/* Profile Section - Bottom Left */}
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
                <p className="text-sm font-medium">Dr. {userType === 'doctor' ? 'Smith' : 'Patient'}</p>
                <p className="text-xs text-indigo-300">{userType}</p>
              </div>
            )}
          </button>

          {showProfile && (
            <div className="absolute bottom-full left-4 mb-2 bg-white text-gray-800 rounded-lg shadow-xl p-2 w-48">
              <button
                onClick={onLogout}
                className="w-full flex items-center gap-2 px-4 py-2 hover:bg-gray-100 rounded text-red-600"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar with Notifications */}
        <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              {userType === 'doctor' ? 'Doctor Dashboard' : 'Patient Portal'}
            </h2>
            <p className="text-gray-600">Welcome back!</p>
          </div>

          {/* Notifications - Top Right */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 hover:bg-gray-100 rounded-full transition"
            >
              <Bell className="w-6 h-6 text-gray-700" />
              <span className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl border z-50">
                <div className="p-4 border-b">
                  <h3 className="font-semibold text-gray-800">Notifications</h3>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  {notifications.map((notif) => (
                    <div key={notif.id} className="p-4 border-b hover:bg-gray-50 cursor-pointer">
                      <p className="text-sm text-gray-800">{notif.text}</p>
                      <p className="text-xs text-gray-500 mt-1">{notif.time}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Center and Right Content */}
        <div className="flex-1 flex overflow-hidden">
          {/* Center - Content based on active page */}
          <div className="flex-1 p-6 overflow-y-auto">
            {activePage === 'dashboard' && userType === 'doctor' && (
              // Doctor Dashboard - Analytics
              <div className="space-y-6">
                <h3 className="text-2xl font-bold text-gray-800">Hospital Analytics</h3>

                {/* Stats Cards */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                    <p className="text-sm opacity-90">Total Patients</p>
                    <p className="text-3xl font-bold mt-2">247</p>
                    <p className="text-sm mt-1">↑ 12% from last month</p>
                  </div>
                  <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white">
                    <p className="text-sm opacity-90">Recovery Rate</p>
                    <p className="text-3xl font-bold mt-2">87%</p>
                    <p className="text-sm mt-1">↑ 5% improvement</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                    <p className="text-sm opacity-90">Avg Wait Time</p>
                    <p className="text-3xl font-bold mt-2">15min</p>
                    <p className="text-sm mt-1">↓ 8min improvement</p>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-2xl shadow-md w-full">
  <div className="flex items-center justify-between mb-4">
    <h2 className="text-xl font-semibold">New vs Follow-Up Patients</h2>

    <div className="flex gap-2">
      <button
        onClick={() => setMode("week")}
        className={`px-3 py-1 rounded-lg border ${
          mode === "week"
            ? "bg-blue-600 text-white"
            : "bg-white text-black border-gray-300"
        }`}
      >
        Weekly
      </button>

      <button
        onClick={() => setMode("month")}
        className={`px-3 py-1 rounded-lg border ${
          mode === "month"
            ? "bg-blue-600 text-white"
            : "bg-white text-black border-gray-300"
        }`}
      >
        Monthly
      </button>
    </div>
  </div>

  <div className="w-full h-64">
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={displayData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="label" />
        <YAxis />
        <Tooltip />
        <Legend />

        <Line
          type="monotone"
          dataKey="new"
          name="New Patients"
          stroke="#2563eb"
          strokeWidth={3}
        />

        <Line
          type="monotone"
          dataKey="followUp"
          name="Follow-Up Patients"
          stroke="#16a34a"
          strokeWidth={3}
        />
      </LineChart>
    </ResponsiveContainer>
  </div>
</div>


                {/* Conditional Risk Analysis */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h4 className="text-lg font-semibold text-gray-800 mb-4">Conditional Risk Analysis</h4>
                  <div className="space-y-3">
                    {[
                      { name: 'John Smith', condition: 'Diabetes Type 2', risk: 'High', score: 85, alert: 'Missed 2 checkups' },
                      { name: 'Michael Brown', condition: 'Heart Disease', risk: 'Critical', score: 92, alert: 'Irregular medication' },
                      { name: 'Emily Davis', condition: 'Asthma', risk: 'Low', score: 28, alert: 'Well managed' },
                      { name: 'Robert Wilson', condition: 'Hypertension', risk: 'Medium', score: 55, alert: 'BP fluctuating' },
                      { name: 'Sarah Johnson', condition: 'Arthritis', risk: 'Low', score: 32, alert: 'Stable condition' },
                    ].map((patient, idx) => (
                      <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 bg-indigo-100 rounded-full flex items-center justify-center">
                            <User className="w-5 h-5 text-indigo-600" />
                          </div>
                          <div>
                            <p className="font-semibold text-gray-800">{patient.name}</p>
                            <p className="text-sm text-gray-600">{patient.condition}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-6">
                          <div className="text-right">
                            <p className="text-xs text-gray-500">Risk Score</p>
                            <p className="text-lg font-bold text-gray-800">{patient.score}</p>
                          </div>
                          <div className="text-right w-32">
                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                              patient.risk === 'Critical' ? 'bg-red-100 text-red-700' :
                              patient.risk === 'High' ? 'bg-orange-100 text-orange-700' :
                              patient.risk === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {patient.risk} Risk
                            </span>
                            <p className="text-xs text-gray-500 mt-1">{patient.alert}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activePage === 'patients' && userType === 'doctor' && (
              // Doctor Patients Page - 3 Patients per Row
              <div className="space-y-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-2xl font-bold text-gray-800">Patients</h3>
                  
                </div>

                <div className="mb-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                    <input
                      type="text"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      placeholder="Search patients..."
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  {PATIENTS_DATA.filter(patient =>
                    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
                  ).map((patient) => (
                    <div key={patient.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
                      <div className="flex flex-col items-center text-center">
                        <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
                          <User className="w-10 h-10 text-indigo-600" />
                        </div>
                        <h4 className="text-lg font-semibold text-gray-800 mb-1">{patient.name}</h4>
                        <p className="text-sm text-gray-600 mb-3">Age: {patient.age}</p>
                        
                        <div className="w-full space-y-2 mb-4">
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-600">Condition:</span>
                            <span className="font-medium text-gray-800">{patient.condition}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-600">Last Visit:</span>
                            <span className="font-medium text-gray-800">{patient.lastVisit}</span>
                          </div>
                        </div>

                        <span className={`px-4 py-1 rounded-full text-xs font-medium ${
                          patient.status === 'Critical' ? 'bg-red-100 text-red-700' :
                          patient.status === 'Monitoring' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-green-100 text-green-700'
                        }`}>
                          {patient.status}
                        </span>

                        <button className="mt-4 w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition text-sm">
                          View Details
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activePage === 'appointments' && userType === 'doctor' && (
              // Appointments Page - Doctor Schedule with Patient and Time
              <div className="space-y-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-2xl font-bold text-gray-800">Appointments</h3>
                 
                </div>

                <div className="space-y-4">
                  {APPOINTMENTS_DATA.map((appointment) => (
                    <div key={appointment.id} className="bg-white rounded-lg shadow-md p-5 hover:shadow-lg transition">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4 flex-1">
                          <div className="w-14 h-14 bg-indigo-100 rounded-full flex items-center justify-center">
                            <User className="w-7 h-7 text-indigo-600" />
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-1">
                              <h4 className="text-lg font-semibold text-gray-800">{appointment.doctor}</h4>
                              <span className="text-sm text-gray-500">•</span>
                              <span className="text-sm font-medium text-indigo-600">{appointment.specialty}</span>
                            </div>
                            <div className="flex items-center gap-4 text-sm text-gray-600">
                              <div className="flex items-center gap-1">
                                <span>Patient: <span className="font-medium text-gray-800">{appointment.patient}</span></span>
                              </div>
                              
                              <div className="flex items-center space-between gap-4 ">
                                <div className="text-right ">
                            <p className="text-lg font-semibold text-gray-800">{appointment.time}</p>
                            <div className="flex items-center gap-1">
                                <span>{appointment.date}</span>
                              </div>
                                 </div>
                              <span className={`px-4 py-2 rounded-full text-sm font-medium ${
                                appointment.status === 'Confirmed' ? 'bg-green-100 text-green-700' :
                                'bg-yellow-100 text-yellow-700'
                              }`}>
                                {appointment.status}
                              </span>
                            </div>
                            </div>
                          </div>
                        </div>
                        
                        
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activePage === 'dashboard' && userType === 'patient' && (
              // Patient Dashboard
              <div className="space-y-6">
                <h3 className="text-2xl font-bold text-gray-800">My Health Dashboard</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                    <p className="text-sm opacity-90">Next Appointment</p>
                    <p className="text-2xl font-bold mt-2">Nov 28</p>
                    <p className="text-sm mt-1">with Dr. Williams</p>
                  </div>
                  <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white">
                    <p className="text-sm opacity-90">Health Score</p>
                    <p className="text-2xl font-bold mt-2">85/100</p>
                    <p className="text-sm mt-1">Good condition</p>
                  </div>
                  <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                    <p className="text-sm opacity-90">Medications</p>
                    <p className="text-2xl font-bold mt-2">3 Active</p>
                    <p className="text-sm mt-1">All up to date</p>
                  </div>
                </div>
                  <div
            className="flex items-center justify-center bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white cursor-pointer"
            onClick={() => setActivePage("form")}
          >
            <p className="text-sm font-semibold opacity-90">Book Appointment</p>
          </div>
              </div>
            )}

             {/* ---------------- APPOINTMENT FORM PAGE ---------------- */}
            {activePage === "form" && (
              <AppointmentForm setActivePage={setActivePage} />
            )}
                </div>
 {activePage === 'appointments' && userType === 'patient' && (
              // Patient Appointment History
              <div className="space-y-6">
                <h3 className="text-2xl font-bold text-gray-800">My Appointment History</h3>
                
                {/* Filter Tabs */}
                <div className="flex gap-2 border-b border-gray-200">
                  <button
                    onClick={() => setAppointmentFilter('all')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      appointmentFilter === 'all'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-600 hover:text-gray-800'
                    }`}
                  >
                    All Appointments
                  </button>
                  <button
                    onClick={() => setAppointmentFilter('confirmed')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      appointmentFilter === 'confirmed'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-600 hover:text-gray-800'
                    }`}
                  >
                    Confirmed
                  </button>
                  <button
                    onClick={() => setAppointmentFilter('pending')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      appointmentFilter === 'pending'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-600 hover:text-gray-800'
                    }`}
                  >
                    Pending
                  </button>
                </div>

                {/* Appointments List */}
                <div className="space-y-4">
                  {APPOINTMENTS_DATA
                    .filter(apt => {
                      // Filter by current patient (John Smith in this case)
                      if (apt.patient !== "John Smith") return false;
                      
                      // Filter by status
                      if (appointmentFilter === 'confirmed') return apt.status === 'Confirmed';
                      if (appointmentFilter === 'pending') return apt.status === 'Pending';
                      return true; // 'all' shows everything
                    })
                    .map(appointment => (
                      <div
                        key={appointment.id}
                        className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <h4 className="text-lg font-bold text-gray-800">
                                {appointment.doctor}
                              </h4>
                              <span
                                className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                  appointment.status === 'Confirmed'
                                    ? 'bg-green-100 text-green-700'
                                    : 'bg-yellow-100 text-yellow-700'
                                }`}
                              >
                                {appointment.status}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600 mb-3">
                              {appointment.specialty}
                            </p>
                            <div className="flex items-center gap-6 text-sm text-gray-700">
                              <div className="flex items-center gap-2">
                                <Calendar className="w-4 h-4 text-blue-600" />
                                <span>{new Date(appointment.date).toLocaleDateString('en-US', { 
                                  month: 'short', 
                                  day: 'numeric', 
                                  year: 'numeric' 
                                })}</span>
                              </div>
                              <div className="flex items-center gap-2">
                                <Clock className="w-4 h-4 text-blue-600" />
                                <span>{appointment.time}</span>
                              </div>
                            </div>
                          </div>
                          <div className="flex gap-2">
                            {appointment.status === 'Confirmed' && (
                              <button className="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                                View Details
                              </button>
                            )}
                            <button className="px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                              Cancel
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  
                  {/* Empty State */}
                  {APPOINTMENTS_DATA.filter(apt => {
                    if (apt.patient !== "John Smith") return false;
                    if (appointmentFilter === 'confirmed') return apt.status === 'Confirmed';
                    if (appointmentFilter === 'pending') return apt.status === 'Pending';
                    return true;
                  }).length === 0 && (
                    <div className="text-center py-12">
                      <Calendar className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-500 text-lg">No appointments found</p>
                      <button
                        onClick={() => setActivePage('bookAppointment')}
                        className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        Book Your First Appointment
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}

{activePage === 'records' && userType === 'patient' && (
              // Medical Reports
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-2xl font-bold text-gray-800">My Medical Reports</h3>
                  
                </div>

                {/* Filter by Type */}
                <div className="flex gap-2 flex-wrap">
                  <button
                    onClick={() => setReportFilter('all')}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                      reportFilter === 'all'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    All Reports
                  </button>
                  <button
                    onClick={() => setReportFilter('Lab Report')}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                      reportFilter === 'Lab Report'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Lab Reports
                  </button>
                  <button
                    onClick={() => setReportFilter('Imaging')}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                      reportFilter === 'Imaging'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Imaging
                  </button>
                  <button
                    onClick={() => setReportFilter('Diagnostic')}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                      reportFilter === 'Diagnostic'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Diagnostic
                  </button>
                </div>

                {/* Reports Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {MEDICAL_REPORTS
                    .filter(report => reportFilter === 'all' || report.type === reportFilter)
                    .map(report => (
                      <div
                        key={report.id}
                        className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-100"
                      >
                        <div className="p-6">
                          <div className="flex items-start justify-between mb-4">
                            <div className="flex items-center gap-3">
                              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                                <FileText className="w-6 h-6 text-blue-600" />
                              </div>
                              <div>
                                <h4 className="font-bold text-gray-800">{report.title}</h4>
                                <p className="text-sm text-gray-500">{report.type}</p>
                              </div>
                            </div>
                            <span
                              className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                report.status === 'Completed'
                                  ? 'bg-green-100 text-green-700'
                                  : 'bg-yellow-100 text-yellow-700'
                              }`}
                            >
                              {report.status}
                            </span>
                          </div>

                          <div className="space-y-3 mb-4">
                            <div className="flex items-center gap-2 text-sm text-gray-600">
                              <Calendar className="w-4 h-4" />
                              <span>{new Date(report.date).toLocaleDateString('en-US', { 
                                month: 'long', 
                                day: 'numeric', 
                                year: 'numeric' 
                              })}</span>
                            </div>
                            <div className="flex items-center gap-2 text-sm text-gray-600">
                              <User className="w-4 h-4" />
                              <span>{report.doctor}</span>
                            </div>
                          </div>

                          <div className="bg-gray-50 rounded-lg p-4 mb-4">
                            <p className="text-sm font-medium text-gray-700 mb-1">Key Findings:</p>
                            <p className="text-sm text-gray-600">{report.findings}</p>
                          </div>

                          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                            <span className="text-xs text-gray-500">{report.fileSize}</span>
                            <div className="flex gap-2">
                              <button className="px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-lg transition-colors flex items-center gap-1">
                                <Eye className="w-4 h-4" />
                                View
                              </button>
                              <button className="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-100 rounded-lg transition-colors flex items-center gap-1">
                                <Download className="w-4 h-4" />
                                Download
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                </div>

                {/* Empty State */}
                {MEDICAL_REPORTS.filter(report => reportFilter === 'all' || report.type === reportFilter).length === 0 && (
                  <div className="text-center py-12">
                    <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500 text-lg">No reports found</p>
                    <p className="text-gray-400 text-sm mt-2">Upload your first medical report to get started</p>
                  </div>
                )}
              </div>
            )}
           

          {/* Right - Chatbot */}
          <div className="w-96 bg-gray-100 p-4">
            <Chatbot />
          </div>
        </div>
      </div>
    </div>
  );
};

// Main App Component
export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userType, setUserType] = useState('');

  const handleLogin = (type) => {
    setUserType(type);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserType('');
  };

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return <Dashboard userType={userType} onLogout={handleLogout} />;
}