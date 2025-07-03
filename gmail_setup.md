# 📧 Gmail Setup Guide for Pool Listener Notifications

## 🔐 Step 1: Enable 2-Factor Authentication

1. Go to your **Google Account**: https://myaccount.google.com/security
2. Click **"2-Step Verification"**
3. Follow the setup process to enable 2FA with your phone

## 🔑 Step 2: Generate App Password

1. Still in **Google Account Security**: https://myaccount.google.com/security
2. Click **"2-Step Verification"** 
3. Scroll down to **"App passwords"**
4. Click **"Generate"** or **"App passwords"**
5. Select **"Mail"** from the dropdown
6. Select **"Other (Custom name)"** 
7. Type: **"Pool Listener"**
8. Click **"Generate"**
9. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

## 🔧 Step 3: Update Your .env File

Edit your `.env` file and replace your EMAIL_PASSWORD:

```env
# Replace this line:
EMAIL_PASSWORD=your_regular_password

# With your App Password (16 characters, no spaces):
EMAIL_PASSWORD=abcdefghijklmnop
```

## ✅ Step 4: Test Notifications

```bash
python test_notifications.py
```

---

## 🆘 If Still Not Working

**Common Issues:**
- **Wrong email format**: Use `yourname@gmail.com` (not `yourname@googlemail.com`)
- **Spaces in App Password**: Remove all spaces from the 16-character password
- **2FA not enabled**: App Passwords only work with 2FA enabled
- **Wrong app password**: Generate a new one if unsure

**Alternative Email Providers:**
If Gmail doesn't work, you can use:
- **Outlook/Hotmail**: `SMTP_SERVER=smtp-mail.outlook.com` `SMTP_PORT=587`
- **Yahoo**: `SMTP_SERVER=smtp.mail.yahoo.com` `SMTP_PORT=587` 