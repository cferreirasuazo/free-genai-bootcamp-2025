import React from "react";
import { NavLink } from "react-router-dom";

const Sidebar: React.FC = () => {
  const links = [
    { path: "/dashboard", label: "Dashboard" },
    { path: "/study-activities", label: "Study Activities" },
    { path: "/words", label: "Words" },
    { path: "/word-groups", label: "Word Groups" },
    { path: "/sessions", label: "Sessions" },
    { path: "/settings", label: "Settings" },
  ];

  return (
    <div className="w-64 h-full bg-gray-100 p-4">
      <h2 className="text-xl font-bold mb-4">LangPortal</h2>
      <nav>
        <ul>
          {links.map((link) => (
            <li key={link.path} className="mb-2">
              <NavLink
                to={link.path}
                className={({ isActive }) =>
                  isActive ? "text-blue-600 font-semibold" : "text-gray-800"
                }
              >
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar; 