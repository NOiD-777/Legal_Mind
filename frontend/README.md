# LegalMind Frontend

A modern, high-performance React/Next.js frontend for AI-powered legal document analysis.

## Features

- ⚡ **Next.js 14** with React 18
- 🎨 **Apple-style Design** with TailwindCSS
- 🎬 **Smooth Animations** with Framer Motion & GSAP
- 📊 **Interactive Charts** with Recharts
- 🌙 **Dark/Light Mode** with next-themes
- 📱 **Responsive Design** for all devices
- ⚖️ **Single & Multi-Model Analysis**
- 🔍 **Detailed Risk Assessments**
- 📈 **Visual Representations** with graphs and charts

## Tech Stack

- **Framework**: Next.js 14
- **UI Library**: React 18
- **Styling**: TailwindCSS 3
- **Animations**: Framer Motion, GSAP
- **Charts**: Recharts
- **Icons**: Lucide React
- **Theme**: next-themes
- **Language**: TypeScript

## Installation

```bash
cd frontend
npm install
```

## Environment Setup

```bash
cp .env.local.example .env.local
```

Update `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── layout.tsx         # Root layout with theme provider
│   ├── page.tsx           # Home page
│   └── analyze/           # Analysis page
├── components/
│   ├── layout/            # Navigation & Footer
│   ├── sections/          # Home sections (Hero, Features)
│   └── analysis/          # Analysis components (Upload, Results)
├── services/              # API client
├── types/                 # TypeScript types
├── styles/                # Global styles
└── public/                # Static assets

## Key Components

### DocumentUpload
- File upload with drag-and-drop
- Model selection (Gemini, Claude, Groq)
- Analysis depth selection
- Focus areas customization

### AnalysisResults
- Risk score visualization
- Bar charts for issue categories
- Pie charts for risk distribution
- Detailed issue breakdowns with GSAP animations

### ComparisonResults
- Multi-model comparison
- Risk score comparison chart
- Confidence levels radar chart
- Model-by-model detailed results

## Animation Features

- **GSAP**: Staggered issue animations, smooth scrolling
- **Framer Motion**: Page transitions, hover effects, scale animations
- **CSS Animations**: Shimmer effects, fade-in/slide-up

## Styling Features

- **Glass Morphism**: Frosted glass effect with backdrop blur
- **Gradient Text**: Modern gradient text effects
- **Dark Mode**: Full dark mode support with system preference detection
- **Responsive**: Mobile-first design approach

## API Integration

The frontend communicates with the Python backend via REST API:

- `POST /analyze` - Single model analysis
- `POST /compare` - Multi-model comparison

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT
