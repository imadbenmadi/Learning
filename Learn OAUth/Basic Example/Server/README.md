# Learn-OAUTH
Sure! Let's walk through the **full authentication process** for a website using **Google OAuth** and **JWT (JSON Web Tokens)** for both first-time visitors (registration) and returning users (login) using **React (frontend)** and **Node.js (backend)**. I'll guide you step by step for both the first-time login and returning user login, including how tokens are stored and verified.

### 1. **Overview of the Process**

1. **First-time visitor**:
   - User visits the site.
   - User clicks "Login with Google" (Google OAuth).
   - User is redirected to Google to sign in.
   - User provides consent to share their Google profile with your app.
   - User is redirected back to your site with a Google OAuth token.
   - Backend verifies the token with Google and creates a JWT.
   - JWT is returned to the frontend and stored (e.g., localStorage).
   - User is now logged in and can access protected resources using the JWT.

2. **Returning user**:
   - User visits the site again.
   - The frontend checks for an existing JWT in localStorage or cookies.
   - If the JWT exists, it's sent to the backend to verify it's valid.
   - If valid, the user is automatically logged in without needing to re-authenticate with Google.
   - If the JWT is expired or invalid, the user will be prompted to log in again with Google.

### 2. **Backend (Node.js) Code**

We'll build an API to handle Google OAuth token verification, JWT generation, and protected routes. This server will:
- Handle user registration/login.
- Return a JWT on successful authentication.
- Provide a route to verify the JWT on returning visits.
- Optionally store user information in a database (like MongoDB, MySQL, etc.).

#### 2.1 **Install Dependencies**

```bash
npm install express google-auth-library jsonwebtoken cors
```

#### 2.2 **Backend Code**

```javascript
const express = require('express');
const { OAuth2Client } = require('google-auth-library');
const jwt = require('jsonwebtoken');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors()); // Enable CORS for cross-origin requests

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'; // Replace with your Google client ID
const JWT_SECRET = 'YOUR_JWT_SECRET'; // Use a strong secret for signing JWTs
const client = new OAuth2Client(CLIENT_ID);

// Simulating a database with in-memory data
let usersDB = [];

// Route to handle Google OAuth token verification and login/registration
app.post('/auth/google', async (req, res) => {
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
    const jwtToken = jwt.sign({ googleId, email, name, picture }, JWT_SECRET, {
      expiresIn: '1h', // Token expires in 1 hour
    });

    // Return JWT token and user data to the frontend
    res.status(200).json({ token: jwtToken, user });
  } catch (error) {
    console.error(error);
    res.status(401).json({ message: 'Invalid Google token' });
  }
});

// Middleware to verify the JWT for protected routes
const verifyJWT = (req, res, next) => {
  const token = req.headers['authorization']?.split(' ')[1]; // Extract token from 'Bearer <token>'

  if (!token) return res.status(401).json({ message: 'Unauthorized' });

  jwt.verify(token, JWT_SECRET, (err, decoded) => {
    if (err) return res.status(403).json({ message: 'Token is invalid or expired' });

    req.user = decoded; // Store the decoded user info in the request
    next();
  });
};

// Protected route example
app.get('/protected', verifyJWT, (req, res) => {
  res.status(200).json({ message: 'Access granted', user: req.user });
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
```

### Explanation of Backend Code:
1. **`/auth/google`**: This route handles the first-time login (registration) and returning login using Google OAuth. If it's a new user, we register them by adding their info to the `usersDB` (simulating a database). A JWT is generated and returned.
2. **`verifyJWT` Middleware**: This middleware protects routes. It verifies the JWT and checks if it's valid. If valid, the request proceeds.
3. **`/protected` Route**: This is an example of a protected route that requires the user to be authenticated.

---

### 3. **Frontend (React) Code**

#### 3.1 **Install Dependencies**

```bash
npm install @react-oauth/google axios
```

#### 3.2 **React Code for Google Login and JWT Handling**

```javascript
import React, { useState, useEffect } from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

const CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'; // Replace with your Google client ID

function App() {
  const [user, setUser] = useState(null);
  const [jwtToken, setJwtToken] = useState('');

  useEffect(() => {
    // Check if JWT is stored in localStorage on component mount
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      verifyToken(storedToken); // Verify the token with the backend
    }
  }, []);

  const handleGoogleLoginSuccess = async (response) => {
    try {
      const googleToken = response.credential; // Get Google ID token

      // Send the Google token to the backend for verification and JWT generation
      const res = await axios.post('http://localhost:5000/auth/google', { token: googleToken });
      const { token, user } = res.data;

      setUser(user); // Set user data
      setJwtToken(token); // Set JWT token
      localStorage.setItem('token', token); // Store JWT in localStorage for future sessions

      console.log('User authenticated', user);
    } catch (error) {
      console.error('Error authenticating with Google', error);
    }
  };

  const verifyToken = async (token) => {
    try {
      const res = await axios.get('http://localhost:5000/protected', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(res.data.user);
      setJwtToken(token);
      console.log('JWT verified, user:', res.data.user);
    } catch (error) {
      console.error('Error verifying token:', error);
      localStorage.removeItem('token'); // Remove invalid token
    }
  };

  const handleLogout = () => {
    setUser(null);
    setJwtToken('');
    localStorage.removeItem('token');
  };

  return (
    <GoogleOAuthProvider clientId={CLIENT_ID}>
      <div className="App">
        <h1>Google OAuth 2.0 in React</h1>

        {!user ? (
          <GoogleLogin
            onSuccess={handleGoogleLoginSuccess}
            onError={() => console.log('Login Failed')}
          />
        ) : (
          <div>
            <h3>Welcome, {user.name}</h3>
            <img src={user.picture} alt={user.name} />
            <button onClick={handleLogout}>Logout</button>
          </div>
        )}
      </div>
    </GoogleOAuthProvider>
  );
}

export default App;
```

### Explanation of React Code:

1. **First-Time User Flow**:
   - The user clicks the **Google Login** button.
   - The frontend gets the Google token and sends it to the backend (`/auth/google`).
   - The backend verifies the token and returns a JWT and user info.
   - The frontend stores the JWT in **localStorage** for future visits.

2. **Returning User Flow**:
   - When the app loads, it checks for a JWT in localStorage.
   - If a token exists, the frontend sends it to the backend (`/protected`) to verify its validity.
   - If the token is valid, the user is automatically logged in.

3. **Logout Flow**:
   - The user clicks the **Logout** button.
   - The JWT is removed from localStorage, and the user state is reset.

---

### 4. **Full Flow of Authentication**

#### First-Time User (New Visitor):
1. User visits the website and clicks "Login with Google."
2. User is redirected to Google's OAuth flow, where they provide consent.
3. Google returns an ID token to the frontend (React).
4. The frontend sends this token to the backend (`/auth/google`).
5. The backend verifies the token, registers the user (if new), and returns a JWT.
6. The frontend stores the JWT in **localStorage** and uses it for future

 API requests.

#### Returning User (Already Registered):
1. User revisits the website.
2. The frontend checks **localStorage** for a JWT.
3. If the JWT exists, it's sent to the backend to verify its validity (`/protected`).
4. If the JWT is valid, the user is logged in automatically.
5. If the JWT is expired or invalid, the user is asked to log in again.

#### Logout:
1. The user clicks the "Logout" button.
2. The JWT is removed from **localStorage**.
3. The user is logged out, and the app state is reset.

---

### 5. **Storing and Managing Tokens**

- **localStorage**: Used to store the JWT so that it persists across page reloads and browser sessions.
- **Session Expiry**: The JWT is set to expire in 1 hour in this example. You can adjust the expiry time based on your app's requirements.
- **Token Refresh**: For production systems, you might implement a **refresh token** strategy where the JWT is refreshed when it expires without requiring the user to log in again.

---

By following these steps, you'll have a complete authentication flow with **Google OAuth** for both first-time visitors and returning users using **React** for the frontend and **Node.js** for the backend.
