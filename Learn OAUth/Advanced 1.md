
Understood! Here’s an advanced version of the authentication and authorization flow without Redis, using JWT rotation, role-based and attribute-based access control (RBAC/ABAC), and context-aware security checks.

---

### Code Enhancements Outline
1. **JWT Rotation with Short-Lived Access Tokens**: Refresh tokens are rotated with each use.
2. **Role-Based and Attribute-Based Access Control (RBAC and ABAC)**: Middleware to enforce both role and attribute-based access.
3. **Context-Aware Security**: Checks the IP and device during login to detect any unusual activity.

---

### Step 1: Setup Models and Utilities

We’ll extend the previous `User` and `Token` models to include attributes for more granular access control.

#### Models: User and Token

```javascript
const { Sequelize, DataTypes } = require('sequelize');

const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASSWORD, {
  host: process.env.DB_HOST,
  dialect: 'mysql',
});

// User model with role and additional attributes
const User = sequelize.define('User', {
  googleId: { type: DataTypes.STRING, unique: true },
  name: DataTypes.STRING,
  email: { type: DataTypes.STRING, unique: true },
  avatar: DataTypes.STRING,
  role: { type: DataTypes.STRING, defaultValue: 'user' }, // e.g., user, admin
  department: DataTypes.STRING, // for attribute-based access control
});

// Token model for refresh tokens with rotation capability
const Token = sequelize.define('Token', {
  userId: { type: DataTypes.INTEGER },
  refreshToken: { type: DataTypes.STRING, unique: true },
  ipAddress: DataTypes.STRING,
  device: DataTypes.STRING,
});

sequelize.sync();
```

### Step 2: JWT Utility Functions with Rotation Logic

Generate and verify tokens. For refresh tokens, use a unique identifier and store it in the database for rotation.

```javascript
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

function generateAccessToken(user) {
  return jwt.sign({ userId: user.id, role: user.role, department: user.department }, process.env.JWT_SECRET, { expiresIn: '15m' });
}

function generateRefreshToken(user) {
  return {
    token: jwt.sign({ userId: user.id }, process.env.JWT_SECRET, { expiresIn: '7d' }),
    id: uuidv4() // Unique ID for refresh token rotation
  };
}
```

### Step 3: Google OAuth with Token Rotation and Context-Aware Security

Extend Google OAuth to store IP and device information with refresh tokens.

```javascript
app.get('/auth/google/callback', async (req, res) => {
  const code = req.query.code;
  const ipAddress = req.ip;
  const device = req.get('User-Agent');

  try {
    const tokenResponse = await axios.post('https://oauth2.googleapis.com/token', {
      code,
      client_id: process.env.GOOGLE_CLIENT_ID,
      client_secret: process.env.GOOGLE_CLIENT_SECRET,
      redirect_uri: process.env.REDIRECT_URI,
      grant_type: 'authorization_code',
    });

    const accessToken = tokenResponse.data.access_token;
    const userResponse = await axios.get('https://www.googleapis.com/oauth2/v2/userinfo', {
      headers: { Authorization: `Bearer ${accessToken}` },
    });

    const { id, name, email, picture } = userResponse.data;
    let user = await User.findOne({ where: { googleId: id } });

    if (!user) {
      user = await User.create({ googleId: id, name, email, avatar: picture });
    }

    const accessTokenJWT = generateAccessToken(user);
    const refreshTokenData = generateRefreshToken(user);

    // Store the refresh token in the database with IP and device info for context-aware security
    await Token.create({ userId: user.id, refreshToken: refreshTokenData.token, ipAddress, device });

    res.cookie('accessToken', accessTokenJWT, { httpOnly: true, maxAge: 15 * 60 * 1000 });
    res.cookie('refreshToken', refreshTokenData.token, { httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000 });
    res.redirect('/dashboard');
  } catch (error) {
    console.error('Error during Google OAuth', error);
    res.redirect('/login');
  }
});
```

### Step 4: Middleware for Role-Based and Attribute-Based Access Control

Use `authorizeRole` middleware to check for user roles and attributes.

```javascript
function authorizeRole(role, attribute = null) {
  return (req, res, next) => {
    const { role: userRole, department } = req.user;

    if (userRole !== role || (attribute && department !== attribute)) {
      return res.status(403).json({ error: 'Access Denied' });
    }

    next();
  };
}

// Usage example: Only admin users in the 'HR' department can access this route
app.get('/admin/hr', authenticateToken, authorizeRole('admin', 'HR'), (req, res) => {
  res.send('Welcome to the HR admin panel');
});
```

### Step 5: Middleware for JWT Rotation and Context-Aware Security

Implement `authenticateToken` middleware to verify tokens, refresh them as needed, and detect unusual IP or device changes.

```javascript
async function authenticateToken(req, res, next) {
  const accessToken = req.cookies.accessToken;
  const refreshToken = req.cookies.refreshToken;
  const ipAddress = req.ip;
  const device = req.get('User-Agent');

  if (!accessToken) return res.status(401).json({ error: 'Access Token Required' });

  jwt.verify(accessToken, process.env.JWT_SECRET, async (err, user) => {
    if (err && refreshToken) {
      try {
        const decoded = jwt.verify(refreshToken, process.env.JWT_SECRET);
        const storedToken = await Token.findOne({ where: { refreshToken } });

        if (!storedToken || storedToken.ipAddress !== ipAddress || storedToken.device !== device) {
          return res.status(403).json({ error: 'Suspicious login detected' });
        }

        // Rotate the refresh token
        const newAccessToken = generateAccessToken(user);
        const newRefreshTokenData = generateRefreshToken(user);

        await Token.update(
          { refreshToken: newRefreshTokenData.token },
          { where: { userId: user.userId } }
        );

        res.cookie('accessToken', newAccessToken, { httpOnly: true, maxAge: 15 * 60 * 1000 });
        res.cookie('refreshToken', newRefreshTokenData.token, { httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000 });
        req.user = user;
        next();
      } catch (refreshError) {
        res.status(403).json({ error: 'Invalid Refresh Token' });
      }
    } else if (user) {
      req.user = user;
      next();
    } else {
      res.status(403).json({ error: 'Access Denied' });
    }
  });
}
```

### Step 6: Logout and Invalidate Tokens

Clear cookies and delete refresh tokens from the database on logout to prevent reuse.

```javascript
app.post('/logout', async (req, res) => {
  const refreshToken = req.cookies.refreshToken;
  if (refreshToken) {
    await Token.destroy({ where: { refreshToken } });
  }
  res.clearCookie('accessToken');
  res.clearCookie('refreshToken');
  res.send('Logged out successfully');
});
```

---

### Summary

1. **JWT Rotation**: Refresh tokens are rotated on each use and updated in the database.
2. **RBAC and ABAC Middleware**: Verifies role and attribute requirements for protected routes.
3. **Context-Aware Security**: Monitors IP and device information associated with refresh tokens to detect unusual activity.
4. **Logout and Invalidation**: Deletes refresh tokens from the database on logout to prevent unauthorized access.

This setup enhances security by detecting suspicious logins, rotating tokens, and implementing granular access control without needing Redis.
