To implement Google OAuth in a Node.js application without Passport, using MySQL and Sequelize, follow this guide to set up the OAuth flow manually.

### 1. **Set Up a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
   - Enable the **Google OAuth API**.
   - Under **Credentials**, create an OAuth 2.0 Client ID. Set the authorized redirect URI (e.g., `http://localhost:3000/auth/google/callback`).

### 2. **Install Required Packages**:
   - You’ll need `express`, `axios` (for making HTTP requests), `sequelize`, `mysql2`, and a session manager like `express-session`.
   - Install them using:
     ```bash
     npm install express axios sequelize mysql2 express-session
     ```

### 3. **Configure Sequelize with MySQL**:
   - Set up Sequelize and define a User model to store user data.

     ```javascript
     const { Sequelize, DataTypes } = require('sequelize');

     const sequelize = new Sequelize('database_name', 'username', 'password', {
       host: 'localhost',
       dialect: 'mysql'
     });

     const User = sequelize.define('User', {
       googleId: {
         type: DataTypes.STRING,
         allowNull: false,
         unique: true
       },
       name: DataTypes.STRING,
       email: DataTypes.STRING,
       avatar: DataTypes.STRING
     });

     sequelize.sync();
     ```

### 4. **Set Up Express and Sessions**:
   - Configure Express, including sessions to manage user sessions.
     ```javascript
     const express = require('express');
     const session = require('express-session');
     const app = express();

     app.use(session({
       secret: 'your-secret-key',
       resave: false,
       saveUninitialized: true,
       cookie: { secure: false } // Set true for HTTPS in production
     }));
     ```

### 5. **Define the OAuth Flow**:
   - Set up routes for starting the OAuth process, handling the callback, and logging out.

#### Step 1: Redirect the User to Google for Authentication
   - In your `/auth/google` route, redirect the user to Google’s OAuth URL with the necessary parameters.

     ```javascript
     const clientID = 'YOUR_GOOGLE_CLIENT_ID';
     const redirectURI = 'http://localhost:3000/auth/google/callback';

     app.get('/auth/google', (req, res) => {
       const googleAuthURL = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientID}&redirect_uri=${redirectURI}&response_type=code&scope=profile email`;
       res.redirect(googleAuthURL);
     });
     ```

#### Step 2: Handle Google’s Callback and Exchange Code for Token
   - In the `/auth/google/callback` route, handle Google’s response, exchange the code for an access token, and retrieve the user’s profile.

     ```javascript
     const axios = require('axios');

     const clientSecret = 'YOUR_GOOGLE_CLIENT_SECRET';

     app.get('/auth/google/callback', async (req, res) => {
       const code = req.query.code;

       try {
         // Exchange authorization code for access token
         const tokenResponse = await axios.post('https://oauth2.googleapis.com/token', {
           code,
           client_id: clientID,
           client_secret: clientSecret,
           redirect_uri: redirectURI,
           grant_type: 'authorization_code'
         });

         const accessToken = tokenResponse.data.access_token;

         // Use the access token to get user info
         const userResponse = await axios.get('https://www.googleapis.com/oauth2/v2/userinfo', {
           headers: { Authorization: `Bearer ${accessToken}` }
         });

         const { id, name, email, picture } = userResponse.data;

         // Check if user exists in the database, otherwise create
         let user = await User.findOne({ where: { googleId: id } });

         if (!user) {
           user = await User.create({
             googleId: id,
             name,
             email,
             avatar: picture
           });
         }

         // Save user ID in session for logged-in state
         req.session.userId = user.id;
         res.redirect('/dashboard');
       } catch (error) {
         console.error('Error during Google OAuth', error);
         res.redirect('/login');
       }
     });
     ```

### 6. **Create Protected Routes and Dashboard**:
   - Only allow access to the dashboard if the user is logged in.
   - You can add middleware to check for a valid session.

     ```javascript
     function isAuthenticated(req, res, next) {
       if (req.session.userId) {
         return next();
       }
       res.redirect('/login');
     }

     app.get('/dashboard', isAuthenticated, async (req, res) => {
       const user = await User.findByPk(req.session.userId);
       res.send(`Welcome ${user.name}`);
     });

     app.get('/logout', (req, res) => {
       req.session.destroy(err => {
         if (err) {
           return res.redirect('/dashboard');
         }
         res.redirect('/');
       });
     });
     ```

### 7. **Launch the Application**:
   - Start your server with:
     ```bash
     node app.js
     ```

### Summary
1. The `/auth/google` route initiates Google OAuth by redirecting the user to Google's login page.
2. Google redirects the user back to `/auth/google/callback` with an authorization code.
3. In `/auth/google/callback`, your app exchanges the code for an access token and retrieves the user profile.
4. The user’s data is saved in the database if it’s their first login, and their ID is stored in the session for authentication.
5. Access to protected routes (like `/dashboard`) is granted only if a valid session exists.
