const express = require("express");
const { OAuth2Client } = require("google-auth-library");
const jwt = require("jsonwebtoken");
const cors = require("cors");

const app = express();
app.use(express.json());

const allowedOrigins = [
    "http://localhost:5173",
    "http://localhost:5173/",
    "http://localhost:5174",
    "http://localhost:5174/",
    // "http://localhost:3500",
];
const corsOptions = {
    origin: (origin, callback) => {
        if (allowedOrigins.indexOf(origin) !== -1 || !origin) {
            callback(null, true);
        } else {
            callback(new Error(`Not allowed by CORS , origin : ${origin}`));
        }
    },
    optionsSuccessStatus: 200,
};
const credentials = (req, res, next) => {
    const origin = req.headers.origin;
    if (allowedOrigins.includes(origin)) {
        res.header("Access-Control-Allow-Credentials", true);
    }
    next();
};
require("dotenv").config();

app.use(credentials);
app.use(cors(corsOptions));
app.use(express.urlencoded({ extended: true }));


const CLIENT_ID =
    "974476086762-ho8ufjo92rj0sqojngqfrtgt6196p3b7.apps.googleusercontent.com"; // Replace with your Google client ID
const JWT_SECRET = "YOUR_JWT_SECRET"; // Use a strong secret for signing JWTs
const client = new OAuth2Client(CLIENT_ID);

// Simulating a database with in-memory data
let usersDB = [];

// Route to handle Google OAuth token verification and login/registration
app.post("/auth/google", async (req, res) => {
    const { token } = req.body;

    try {
        // Verify the Google token
        const ticket = await client.verifyIdToken({
            idToken: token,
            audience: CLIENT_ID,
        });

        const payload = ticket.getPayload();
        const { sub: googleId, email, name, picture } = payload; // 'sub' is the unique Google ID

        // Check if the user already exists in the "database"
        let user = usersDB.find((u) => u.googleId === googleId);

        if (!user) {
            // New user: Register them
            user = { googleId, email, name, picture };
            usersDB.push(user);
        }

        // Generate a JWT token for the session
        const jwtToken = jwt.sign(
            { googleId, email, name, picture },
            JWT_SECRET,
            {
                expiresIn: "1h", // Token expires in 1 hour
            }
        );

        // Return JWT token and user data to the frontend
        res.status(200).json({ token: jwtToken, user });
    } catch (error) {
        console.error(error);
        res.status(401).json({ message: "Invalid Google token" });
    }
});

// Middleware to verify the JWT for protected routes
const verifyJWT = (req, res, next) => {
    const token = req.headers["authorization"]?.split(" ")[1]; // Extract token from 'Bearer <token>'

    if (!token) return res.status(401).json({ message: "Unauthorized" });

    jwt.verify(token, JWT_SECRET, (err, decoded) => {
        if (err)
            return res
                .status(403)
                .json({ message: "Token is invalid or expired" });

        req.user = decoded; // Store the decoded user info in the request
        next();
    });
};

// Protected route example
app.get("/protected", verifyJWT, (req, res) => {
    res.status(200).json({ message: "Access granted", user: req.user });
});

// Start the server
const PORT =  5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
