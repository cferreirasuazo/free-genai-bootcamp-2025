import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Dashboard from "@/pages/Dashboard";
import Words from "@/pages/Words";
import WordDetails from "@/pages/WordDetails";
import Sidebar from "@/components/Sidebar";
import "./App.css";

export default function App() {
  return (
    <Router>
      <div className="flex min-h-screen">
        {/* Sidebar: Fixed width, does not scroll */}
        <Sidebar />

        {/* Main content: Scrollable */}
        <div className="flex-1 p-8 bg-gray-50 overflow-auto">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/words" element={<Words />} />
            <Route path="/words/:id" element={<WordDetails />} />
            {/* Add more routes as needed */}
          </Routes>
        </div>
      </div>
    </Router>
  );
}
