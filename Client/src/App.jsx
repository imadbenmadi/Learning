import React, { useState, useEffect } from "react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import axios from "axios";

const CLIENT_ID =
    "974476086762-ho8ufjo92rj0sqojngqfrtgt6196p3b7.apps.googleusercontent.com"; // Replace with your Google client ID

function App() {
    const [user, setUser] = useState(null);
    const [jwtToken, setJwtToken] = useState("");

    useEffect(() => {
        // Check if JWT is stored in localStorage on component mount
        const storedToken = localStorage.getItem("token");
        if (storedToken) {
            verifyToken(storedToken); // Verify the token with the backend
        }
    }, []);
    useEffect(() => {
        console.log("user", user);
    }, [user]);

    const handleGoogleLoginSuccess = async (response) => {
        try {
            const googleToken = response.credential; // Get Google ID token

            // Send the Google token to the backend for verification and JWT generation
            const res = await axios.post("http://localhost:5000/auth/google", {
                token: googleToken,
            });
            const { token, user } = res.data;

            setUser(user); // Set user data
            setJwtToken(token); // Set JWT token
            localStorage.setItem("token", token); // Store JWT in localStorage for future sessions

            console.log("User authenticated", user);
        } catch (error) {
            console.error("Error authenticating with Google", error);
        }
    };

    const verifyToken = async (token) => {
        try {
            const res = await axios.get("http://localhost:5000/protected", {
                headers: { Authorization: `Bearer ${token}` },
            });
            setUser(res.data.user);
            setJwtToken(token);
            console.log("JWT verified, user:", res.data.user);
        } catch (error) {
            console.error("Error verifying token:", error);
            localStorage.removeItem("token"); // Remove invalid token
        }
    };

    const handleLogout = () => {
        setUser(null);
        setJwtToken("");
        localStorage.removeItem("token");
    };

    return (
        <GoogleOAuthProvider clientId={CLIENT_ID}>
            <div className="App">
                <h1>Google OAuth 2.0 in React</h1>

                {!user ? (
                    <GoogleLogin
                        onSuccess={handleGoogleLoginSuccess}
                        onError={() => console.log("Login Failed")}
                    />
                ) : (
                    <div>
                        <h3>Welcome, {user.name}</h3>
                        <img
                            src={user.picture}
                            alt={user.name}
                        />
                        <button onClick={handleLogout}>Logout</button>
                    </div>
                )}
            </div>
        </GoogleOAuthProvider>
    );
}

export default App;
