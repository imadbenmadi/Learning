// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App"; // Ensure this path points to your renamed main component
import "./index.css"; // Tailwind styles

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);