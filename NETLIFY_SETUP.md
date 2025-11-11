# Netlify Deployment with Google OAuth

This guide walks you through deploying your Quartz site to Netlify with Google OAuth authentication.

## 🎯 What You're Setting Up

```
GitHub Repo → Netlify Build → Protected Site with Google Login
     ↑
Your workflow stays the same!
(Claude Code, git push, etc.)
```

---

## 📋 Prerequisites

- ✅ Netlify account (you have this!)
- ✅ GitHub account with this repo
- ✅ Google account (for OAuth)

---

## 🚀 Step 1: Connect GitHub to Netlify

### Option A: Import from Dashboard (Easiest)

1. Go to [Netlify Dashboard](https://app.netlify.com/)
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **"Deploy with GitHub"**
4. Authorize Netlify to access your GitHub account
5. Select the `SteamEngine25` repository
6. **Build settings** (should auto-detect from netlify.toml):
   ```
   Build command: npx quartz build
   Publish directory: public
   ```
7. Click **"Deploy site"**

### Option B: Netlify CLI (If you prefer terminal)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize in your repo
cd /path/to/SteamEngine25
netlify init

# Follow prompts:
# - Create & configure new site
# - Link to GitHub repo
# - Build command: npx quartz build
# - Publish directory: public
```

---

## 🎨 Step 2: Configure Your Site

After deployment, Netlify gives you a URL like: `random-name-123.netlify.app`

### Change Site Name (Optional)

1. Go to **Site settings** → **General** → **Site details**
2. Click **"Change site name"**
3. Enter: `steamengine25` (or whatever you want)
4. Your site becomes: `steamengine25.netlify.app`

### Update Your Config

Update `quartz.config.ts` with your actual Netlify URL:

```typescript
baseUrl: "steamengine25.netlify.app",  // Or your custom domain
```

Commit and push this change:

```bash
git add quartz.config.ts
git commit -m "Update baseUrl for Netlify"
git push
```

---

## 🔐 Step 3: Enable Netlify Identity

This is what enables authentication!

1. Go to your site dashboard
2. Navigate to **"Identity"** tab (in the top menu)
3. Click **"Enable Identity"**

**🎉 Identity is now enabled!**

---

## 🔑 Step 4: Configure Google OAuth

### Enable Google as Provider

1. Still in **Identity** tab, click **"Settings and usage"**
2. Scroll to **"External providers"**
3. Click **"Add provider"**
4. Select **"Google"**

### Get Google OAuth Credentials

You need to create OAuth credentials in Google Cloud Console:

#### 4a. Create Google OAuth App

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Navigate to **"APIs & Services"** → **"Credentials"**
4. Click **"Create Credentials"** → **"OAuth client ID"**
5. Choose **"Web application"**
6. Configure:
   ```
   Name: SteamEngine25 Netlify Auth

   Authorized JavaScript origins:
   https://steamengine25.netlify.app

   Authorized redirect URIs:
   https://steamengine25.netlify.app/.netlify/identity/callback
   ```
7. Click **"Create"**
8. Copy the **Client ID** and **Client Secret**

#### 4b. Add Credentials to Netlify

1. Back in Netlify Identity settings
2. In the Google provider configuration, paste:
   - **Client ID**: (from Google)
   - **Client Secret**: (from Google)
3. Click **"Install provider"**

**🎉 Google OAuth is now active!**

---

## 🎯 Step 5: Configure Access Control

You have three options for who can access your site:

### Option A: Invite Only (Recommended)

**Best for: Personal sites or small teams**

1. Go to **Identity** → **Settings**
2. Under **"Registration preferences"**:
   - Select **"Invite only"**
3. To invite users:
   - Go to **Identity** tab
   - Click **"Invite users"**
   - Enter email addresses (must have Google accounts)
   - Click **"Send"**

They'll receive an invite email and can log in with Google!

### Option B: Open Registration + Email Whitelist

**Best for: Allowing specific domains (like @company.com)**

1. Go to **Identity** → **Settings**
2. Under **"Registration preferences"**:
   - Select **"Open"**
3. Under **"Email allowlist"**:
   - Enter allowed emails or domains:
   ```
   yourfriend@gmail.com
   another@gmail.com
   @yourcompany.com  ← Allows entire domain
   ```

### Option C: Open Registration

**Not recommended** - Anyone can sign up!

---

## 🧪 Step 6: Test Authentication

### Test It Out

1. Open your site in an **incognito window**: `https://steamengine25.netlify.app`
2. You should see the Netlify Identity login modal appear
3. Click **"Continue with Google"**
4. Authorize with your Google account
5. You should be redirected back to your site
6. **You're in!** 🎉

### Test Logout

1. The Netlify Identity widget should show in the corner (or you can trigger it)
2. Click your profile → **"Log out"**
3. You should be prompted to log back in

### Add Logout Button (Optional)

Want a visible logout button? Add this to your site:

```html
<button onclick="netlifyIdentity.logout()">Logout</button>
```

---

## 🎨 Step 7: Customize Identity Widget (Optional)

Make the login modal match your site's branding:

1. Go to **Identity** → **Settings**
2. Scroll to **"Site information"**
3. Customize:
   - **Site name**: "SteamEngine25"
   - **Logo URL**: Link to your logo
   - **Accent color**: Match your theme

---

## 🔄 Your New Workflow

**Nothing changes for you!** Here's your workflow:

```bash
# 1. Edit your notes in Obsidian
# 2. Copy to content/
cp /path/to/Obsidian/*.md content/

# 3. Push to GitHub (same as before!)
git add content/
git commit -m "Add new notes"
git push

# 4. Netlify automatically:
#    - Detects the push
#    - Runs the build
#    - Deploys your site
#    - Maintains authentication

# 5. Visit your protected site!
# https://steamengine25.netlify.app
```

**Claude Code still works perfectly!** ✅

---

## 🔍 Viewing Who's Logged In

Track your users:

1. Go to **Identity** tab
2. See all registered/invited users
3. See who's logged in
4. Manually add/remove users
5. See login history

---

## 🚨 Troubleshooting

### "Build failed"

**Check Netlify build logs:**
1. Go to **Deploys** tab
2. Click the failed deploy
3. View logs to see error

**Common fixes:**
- Make sure `netlify.toml` is in root directory
- Verify Node version is 22
- Check for syntax errors in `.ts` files

### "Login modal doesn't appear"

**Check:**
1. Is Identity enabled in Netlify dashboard?
2. Clear browser cache and try incognito
3. Check browser console for errors (F12)
4. Verify the script is loaded: View source → Search for "netlify-identity-widget"

### "Google OAuth not working"

**Check:**
1. Google OAuth credentials are correctly entered in Netlify
2. Redirect URI in Google Console matches: `https://your-site.netlify.app/.netlify/identity/callback`
3. Authorized JavaScript origins includes: `https://your-site.netlify.app`

### "User can't access site even after login"

**Check:**
1. Is the user invited? (if using invite-only)
2. Is their email whitelisted? (if using email allowlist)
3. Try having them log out and log back in

### "Changes not showing up"

**Wait for deploy:**
1. Check **Deploys** tab
2. Latest deploy should show "Published" with green checkmark
3. Typically takes 1-2 minutes
4. Hard refresh browser: Ctrl+Shift+R (Windows) / Cmd+Shift+R (Mac)

---

## 💡 Advanced: Custom Domain

Want to use your own domain instead of `*.netlify.app`?

### Setup Custom Domain

1. Buy a domain (Namecheap, Google Domains, etc.)
2. In Netlify: **Domain settings** → **Add custom domain**
3. Enter your domain: `example.com`
4. Follow DNS configuration instructions
5. Netlify provides automatic HTTPS!

### Update Your Config

After setting custom domain:

```typescript
// quartz.config.ts
baseUrl: "example.com",  // Your custom domain
```

### Update Google OAuth

Don't forget to update Google Console:
1. Add your custom domain to **Authorized JavaScript origins**
2. Add `https://example.com/.netlify/identity/callback` to redirect URIs

---

## 📊 Monitoring & Analytics

### Build Status

Monitor builds in **Deploys** tab:
- Green ✅ = Success
- Red ❌ = Failed
- Yellow 🟡 = Building

### Analytics

Netlify includes basic analytics:
- **Analytics** tab in dashboard
- See pageviews, unique visitors
- Top pages
- Bandwidth usage

### Notifications

Get notified of deploys:
1. **Site settings** → **Build & deploy** → **Deploy notifications**
2. Add:
   - Email notifications
   - Slack notifications
   - Webhook notifications

---

## 🎯 Quick Reference

### Useful URLs

- **Netlify Dashboard**: https://app.netlify.com/
- **Your Site**: https://steamengine25.netlify.app
- **Google Cloud Console**: https://console.cloud.google.com/
- **Netlify Docs**: https://docs.netlify.com/

### Key Netlify Settings Locations

```
Site Dashboard → Identity
  ↓
  ├── Enable Identity
  ├── Settings → External providers → Google
  ├── Settings → Registration → Invite only
  └── Invite users

Site Dashboard → Domain settings
  └── Custom domain configuration

Site Dashboard → Deploys
  └── View build logs and status
```

---

## 🎉 You're Done!

Your site now has:
- ✅ Google OAuth authentication
- ✅ Whitelist control (who can access)
- ✅ Automatic deployments from GitHub
- ✅ Free hosting + SSL
- ✅ Fast global CDN
- ✅ Same development workflow

**Questions?** Check:
- [Netlify Identity Docs](https://docs.netlify.com/visitor-access/identity/)
- [Google OAuth Setup](https://developers.google.com/identity/protocols/oauth2)

**Happy publishing! 🚀**
