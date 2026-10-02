# Resume Parser Using AI - Setup Guide

## Project Overview
This is a full-stack application that parses resumes using AI and matches them against job descriptions. The project consists of three main components:

- **Frontend**: React + Vite web interface
- **Backend**: Express.js API server
- **Python AI Module**: Flask API with spaCy NER model for resume parsing

---

## Prerequisites

Before starting, ensure you have the following installed on your system:

### Required Software
- **Node.js**: v16 or higher ([Download](https://nodejs.org/))
- **Python**: v3.8 or higher ([Download](https://www.python.org/))
- **MongoDB**: Local or Atlas cloud instance ([Download](https://www.mongodb.com/products/platform/atlas) or [Local](https://www.mongodb.com/try/download/community))
- **Git**: For version control

### Required Accounts
- **MongoDB Atlas**: Cloud database ([Create Account](https://www.mongodb.com/cloud/atlas))

---

## Environment Setup

### 1. Backend Environment Configuration

Create a `.env` file in the `backend/` directory:

```bash
# backend/.env

# MongoDB Connection URI
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority

# Server Configuration
PORT=5000
NODE_ENV=development

# Python API Configuration
PYTHON_API_URL=http://localhost:5001
```

**Getting Credentials:**
- **MongoDB URI**: From MongoDB Atlas dashboard → Connect → Copy connection string

### 2. Python Environment Configuration

Create a `.env` file in the `Resume_Parser/` directory (optional):

```bash
# Resume_Parser/.env

FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5001
```

---

## Installation Steps

### Step 1: Install Backend Dependencies

```bash
# Navigate to backend directory
cd backend

# Install Node packages
npm install

# Verify installation
npm list
```

### Step 2: Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install Node packages
npm install

# Verify installation
npm list
```

### Step 3: Set Up Python Environment

```bash
# Navigate to Resume_Parser directory
cd Resume_Parser

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirement.txt

# Download spaCy model data (if not already in TrainedModel/)
python -m spacy download en_core_web_sm

# Verify installation
pip list
```

---

## Database Setup

### MongoDB Atlas Setup (Recommended for Cloud)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster (Free tier available)
3. Add a Database User with username and password
4. Whitelist your IP address (or 0.0.0.0 for all)
5. Get your connection string from "Connect" button
6. Use this string in your `.env` file as `MONGODB_URI`

### Local MongoDB Setup

1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```bash
   # Windows (if installed via installer)
   net start MongoDB
   
   # Or run mongod directly
   mongod
   ```
3. Use connection string: `mongodb://localhost:27017/resume-parser`

---

## Running the Application

### Terminal 1: Start Backend Server

```bash
cd backend
npm start
# or if you have a start script in package.json

# Server will run on http://localhost:5000
```

If there's no start script, you may need to create one or run:
```bash
node server.js
```

### Terminal 2: Start Python API Server

```bash
cd Resume_Parser

# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Start Flask application
python main.py
# Flask server will run on http://localhost:5001
```

### Terminal 3: Start Frontend Development Server

```bash
cd frontend

# Start Vite dev server
npm run dev
# Frontend will run on http://localhost:5173
```

---

## Accessing the Application

Once all three servers are running:

- **Frontend**: Open browser and go to `http://localhost:5173`
- **Backend API**: Available at `http://localhost:5000/api`
- **Python API**: Available at `http://localhost:5001`

---

## Project Structure

```
Resume-Parser-Using-AI/
├── backend/                    # Express.js API server
│   ├── config/                # Database configuration
│   ├── controllers/           # Request handlers
│   ├── models/                # MongoDB schemas
│   ├── routes/                # API endpoints
│   ├── server.js              # Express app entry point
│   ├── package.json
│   └── .env                   # Environment variables
│
├── frontend/                   # React + Vite application
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/             # Page components
│   │   ├── utils/             # Utility functions and API calls
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
└── Resume_Parser/              # Python AI module
    ├── main.py                # Flask API entry point
    ├── processor.py           # PDF processing logic
    ├── calculate_score.py     # Matching score calculation
    ├── extractors.py          # Data extraction utilities
    ├── requirement.txt        # Python dependencies
    ├── data/                  # CSV data files (skills, positions, majors)
    ├── TrainedModel/          # Pre-trained spaCy NER model
    └── input/                 # Input PDFs directory
```

---

## Key API Endpoints

### Backend API (Node.js)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload resume PDF |
| GET | `/resumes` | Get all uploaded resumes |
| GET | `/matching-scores` | Calculate matching scores |

### Python API (Flask)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/calculate-matching-scores` | Calculate resume-to-JD matching |
| POST | `/extract-resume` | Extract information from resume |

---

## Troubleshooting

### Backend Issues

**Problem**: `MONGODB_URI is not defined`
- **Solution**: Ensure `.env` file exists in `backend/` with correct `MONGODB_URI`

**Problem**: `Cannot connect to MongoDB`
- **Solution**: 
  - Verify MongoDB is running
  - Check connection string syntax
  - Ensure IP is whitelisted in MongoDB Atlas

**Problem**: CORS errors in console
- **Solution**: CORS is already enabled in `server.js`. Check if backend is running on correct port.

**Problem**: Port 5000 already in use
- **Solution**: 
  ```bash
  # Find and kill process using port 5000
  # Windows (PowerShell):
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  
  # Or change PORT in .env file
  ```

### Frontend Issues

**Problem**: `npm install fails`
- **Solution**: 
  ```bash
  # Clear npm cache
  npm cache clean --force
  # Then retry
  npm install
  ```

**Problem**: Port 5173 already in use
- **Solution**: 
  ```bash
  # Vite will automatically try next available port
  # Or modify vite.config.js to specify different port
  ```

### Python Issues

**Problem**: `ModuleNotFoundError: No module named 'spacy'`
- **Solution**:
  ```bash
  # Activate virtual environment first
  venv\Scripts\activate  # Windows
  # Then reinstall
  pip install -r requirement.txt
  ```

**Problem**: `Port 5001 already in use`
- **Solution**:
  ```bash
  # Find and kill process using port 5001
  # Windows (PowerShell):
  netstat -ano | findstr :5001
  taskkill /PID <PID> /F
  ```

**Problem**: Spacy model not found
- **Solution**:
  ```bash
  # Download the model
  python -m spacy download en_core_web_sm
  ```

---

## File Uploads

Uploaded resumes and job descriptions are stored in `backend/upload/` and served at `/upload/<filename>`. No external account is required.

---

## Production Deployment

### Before Deploying:

1. **Set Environment Variables**: Update `.env` for production URLs
2. **Build Frontend**:
   ```bash
   cd frontend
   npm run build
   # Creates optimized `dist/` folder
   ```
3. **Security Checklist**:
   - Never commit `.env` files to repository
   - Use strong MongoDB passwords
   - Enable HTTPS in production

### Deployment Platforms:
- **Backend**: Heroku, Railway, AWS, DigitalOcean
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Python API**: Heroku, Railway, AWS Lambda
- **Database**: MongoDB Atlas (managed cloud service)

---

## Development Commands

```bash
# Backend
npm start              # Start server
npm run dev           # Development mode (if configured)

# Frontend
npm run dev           # Start dev server
npm run build         # Build for production
npm run preview       # Preview production build
npm run lint          # Run ESLint

# Python
python main.py        # Start Flask server
pip install -r requirement.txt  # Install dependencies
python -m spacy download en_core_web_sm  # Download spacy model
```

---

## Testing the Setup

Once all servers are running:

1. Open `http://localhost:5173` in your browser
2. Upload a resume PDF
3. Enter a job description
4. Click "Analyze" to see matching scores
5. Check console for any errors

---

## Additional Resources

- [Node.js Documentation](https://nodejs.org/docs/)
- [Express.js Guide](https://expressjs.com/)
- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Python Documentation](https://docs.python.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [spaCy Documentation](https://spacy.io/)

---

## Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review error logs in console
3. Verify all environment variables are set correctly
4. Ensure all services (MongoDB, API servers) are running

---

## Next Steps

After successful setup:
1. Explore the frontend UI
2. Test resume upload functionality
3. Review the database schema in MongoDB
4. Examine the trained spaCy model in `Resume_Parser/TrainedModel/`
5. Customize job descriptions and skills data in `Resume_Parser/data/`

---

**Happy Resume Parsing! 🚀**
