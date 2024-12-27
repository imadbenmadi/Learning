// server.js
const express = require("express");
const app = express();
const dotenv = require("dotenv");
const path = require("path");

dotenv.config();

app.get("/", (req, res) => {
    res.json({
        message: "Welcome to the API",
    });
});

// Root route
app.get("/", (req, res) => {
    res.send("Hello from Task");
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;
