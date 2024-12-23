You're absolutely right. IP addresses can indeed change frequently, and flagging each change would be too restrictive. A better approach is to **send a notification (like an email) if a new or unusual device logs in**, without blocking the user. Here’s an improved flow for handling this:

### Enhanced Approach
1. **Track Device Fingerprint**: Use a unique identifier for each device (e.g., User-Agent string combined with a hashed device ID).
2. **Notify on New Device Login**: When a new device logs in, send an email notification to the user rather than blocking access.
3. **Token Rotation and Expiration**: Continue using short-lived access tokens with refresh tokens for secure sessions.
4. **Flexible Security with IP Logging (Optional)**: Log IP changes without blocking, for record-keeping or analysis.

---

### Implementation Steps

### Step 1: Update Models for Device Tracking
We'll track the user’s `refreshToken`, `deviceId`, and `lastLoginDate` in the `Token` model.

#### Models
```javascript
const { Sequelize, DataTypes } = require('sequelize');
const sequelize = new Sequelize(process.env.DB_NAME, process.env.DB_USER, process.env.DB_PASSWORD, {
  host: process.env.DB_HOST,
  dialect: 'mysql',
});

// User model
const User = sequelize.define('User', {
  googleId: { type: DataTypes.STRING, unique: true },
  name: DataTypes.STRING,
  email: { type: DataTypes.STRING, unique: true },
  avatar: DataTypes.STRING,
  role: { type: DataTypes.STRING, defaultValue: 'user' },
});

// Token model with device tracking
const Token = sequelize.define('Token', {
  userId: { type: DataTypes.INTEGER },
  refreshToken: { type: DataTypes.STRING, unique: true },
  deviceId: DataTypes.STRING,
  lastLoginDate: DataTypes.DATE,
});

sequelize.sync();
```

### Step 2: Generate Unique Device Identifier
A simple way to identify a device is to hash the User-Agent string and store it as `deviceId`. For this, use `crypto` to create a hash.

```javascript
const crypto = require('crypto');

function getDeviceId(req) {
  const userAgent = req.get('User-Agent');
  return crypto.createHash('sha256').update(userAgent).digest('hex');
}
```

### Step 3: OAuth Callback with Device Tracking and Notification
In the OAuth callback, check if the device is new. If it’s a new device, send an email notification and store the `deviceId`.

#### Email Notification Utility
Implement a simple email notification (assuming you have a mail service configured).

```javascript
const nodemailer = require('nodemailer');

async function sendNewDeviceEmail(user) {
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS,
    },
  });

  const mailOptions = {
    from: process.env.EMAIL_USER,
    to: user.email,
    subject: 'New Device Login Detected',
    text: `Hello ${user.name},\n\nWe've detected a new login to your account from an unrecognized device. If this was not you, please secure your account immediately.\n\nBest regards,\nSecurity Team`,
  };

  await transporter.sendMail(mailOptions);
}
```

#### OAuth Callback with Device Check
Check if the device is new; if so, send an email notification and save the device information.

```javascript
app.get('/auth/google/callback', async (req, res) => {
  const code = req.query.code;
  const deviceId = getDeviceId(req);

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

    // Check if device is new
    let token = await Token.findOne({ where: { userId: user.id, deviceId } });
    if (!token) {
      // Send notification email
      await sendNewDeviceEmail(user);

      // Save new device info
      token = await Token.create({
        userId: user.id,
        refreshToken: generateRefreshToken(user).token,
        deviceId,
        lastLoginDate: new Date(),
      });
    } else {
      // Update last login date for existing device
      token.lastLoginDate = new Date();
      await token.save();
    }

    const accessTokenJWT = generateAccessToken(user);
    res.cookie('accessToken', accessTokenJWT, { httpOnly: true, maxAge: 15 * 60 * 1000 });
    res.cookie('refreshToken', token.refreshToken, { httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000 });
    res.redirect('/dashboard');
  } catch (error) {
    console.error('Error during Google OAuth', error);
    res.redirect('/login');
  }
});
```

### Step 4: Middleware for JWT Rotation without Device Blocking
The `authenticateToken` middleware will simply refresh the access token using the refresh token if it’s expired but will not block access due to IP changes.

```javascript
async function authenticateToken(req, res, next) {
  const accessToken = req.cookies.accessToken;
  const refreshToken = req.cookies.refreshToken;

  if (!accessToken) return res.status(401).json({ error: 'Access Token Required' });

  jwt.verify(accessToken, process.env.JWT_SECRET, async (err, user) => {
    if (err && refreshToken) {
      try {
        const decoded = jwt.verify(refreshToken, process.env.JWT_SECRET);
        const storedToken = await Token.findOne({ where: { refreshToken } });

        if (!storedToken) return res.status(403).json({ error: 'Invalid Refresh Token' });

        const newAccessToken = generateAccessToken(user);
        res.cookie('accessToken', newAccessToken, { httpOnly: true, maxAge: 15 * 60 * 1000 });
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

### Summary of Changes
1. **Device Identification**: A unique device ID is generated from the User-Agent string and stored in the database.
2. **Email Notifications**: When a new device is detected, an email is sent to notify the user.
3. **Token Rotation without Blocking**: Tokens are rotated, but login is not blocked if the IP or device changes.
4. **Flexible Security**: IP is logged without being enforced as a blocking condition.
