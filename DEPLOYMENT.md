# Deployment Guide

## 🔍 Local Testing with pgAdmin

### Database Connection Details:
- **Host**: localhost
- **Port**: 5432
- **Database**: student_db
- **Username**: postgres
- **Password**: Vi1279_@2004

### Steps:
1. Open your local pgAdmin
2. Create new server connection with above details
3. Navigate to student_db → Schemas → public → Tables → students
4. Right-click students table → "View/Edit Data" → "All Rows"
5. You should see 5 sample students

## 🚀 Render Deployment

### Prerequisites:
1. GitHub account
2. Render account (free tier available)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Student Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/student-management.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click "New" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically:
   - Create PostgreSQL database
   - Deploy the web service
   - Set up environment variables

### Step 3: Access Your Deployed App
- Your app will be available at: `https://student-management-api.onrender.com`
- Database will be automatically provisioned and connected

### Step 4: Initialize Database (if needed)
If the database is empty after deployment:
1. Go to Render dashboard
2. Open your web service
3. Go to "Shell" tab
4. Run: `python -c "from app import init_db; init_db()"`

## 🔧 Environment Variables (Auto-configured)
- `DATABASE_URL`: Automatically set by Render
- `PORT`: Automatically set by Render

## 📊 Monitoring on Render
- View logs in Render dashboard
- Monitor performance metrics
- Set up alerts for downtime

## 🌐 Production URLs
- **Web App**: https://your-app-name.onrender.com
- **API Endpoints**: 
  - GET /students
  - POST /students
  - PUT /students/{id}
  - DELETE /students/{id}

## 🔒 Security Notes
- Database credentials are automatically managed by Render
- HTTPS is enabled by default
- Environment variables are encrypted