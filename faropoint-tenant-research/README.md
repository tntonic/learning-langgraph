# Faropoint Tenant Research System

A modern React application for researching and evaluating potential commercial real estate tenants using AI-powered analysis.

## Features

- 🔍 **Comprehensive Tenant Research** - Analyzes multiple data sources to evaluate potential tenants
- 📊 **Visual Scoring System** - Clear visualization of tenant quality scores
- 🚀 **Real-time Progress Tracking** - Watch the AI analyze each aspect of the tenant
- 💼 **Professional Reports** - Detailed reports with strengths, concerns, and recommendations
- 🎨 **Modern UI** - Built with React, TypeScript, and Tailwind CSS

## Screenshots

### Research Form
Enter a company name and location to begin the analysis.

### Progress Tracking
Real-time updates as the system analyzes:
- Company Identification
- Online Presence Analysis
- Business Verification
- Financial Indicators
- Real Estate History
- Risk Assessment
- Tenant Scoring
- Report Generation

### Results Dashboard
- Overall tenant score (0-100)
- Recommendation (Highly Recommended, Recommended, Proceed with Caution, Not Recommended)
- Score breakdown (Stability, Growth, Risk, Reputation)
- Key metrics and business verification
- Strengths and concerns analysis

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+ (for backend API)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

### Running with Backend API

1. Install Python dependencies:
```bash
pip install fastapi uvicorn sse-starlette
```

2. Start the API server:
```bash
python ../faropoint_api.py
```

3. Set the API URL in your environment:
```bash
REACT_APP_API_URL=http://localhost:8000 npm start
```

## Technology Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Icons**: React Icons
- **HTTP Client**: Axios
- **Backend**: FastAPI (Python)
- **AI Workflow**: LangGraph

## API Integration

The app can work in two modes:

1. **Demo Mode** (default) - Uses simulated data for testing
2. **API Mode** - Connects to the FastAPI backend for real tenant research

To use the real API, ensure the backend is running and set the `REACT_APP_API_URL` environment variable.

## Project Structure

```
src/
├── components/
│   ├── TenantSearchForm.tsx    # Search input form
│   ├── WorkflowProgress.tsx    # Progress indicator
│   └── ResearchResults.tsx     # Results display
├── services/
│   └── api.ts                  # API integration
├── types/
│   └── index.ts               # TypeScript types
└── App.tsx                    # Main application
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary to Faropoint.