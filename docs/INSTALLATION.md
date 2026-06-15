# 📚 Installation Guide

## Prerequisites

- Node.js >= 14
- npm or yarn

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/kunalmavani01-boop/PROMPTER.git
cd PROMPTER
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment (Optional)

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_GEMINI_API_KEY=your_key_here
```

### 4. Start Application

**Development:**
```bash
npm run dev
```

**Production:**
```bash
npm run build
npm start
```

## Accessing PROMPTER

- **Local**: http://localhost:3000
- **Development**: http://localhost:3000 (with hot reload)

## Deployment

### Deploy to Vercel

```bash
npm i -g vercel
vercel
```

### Deploy to Netlify

```bash
npm run build
# Upload 'out' folder to Netlify
```

## Troubleshooting

### Port 3000 Already in Use

```bash
npm run dev -- -p 3001
```

### Dependency Issues

```bash
rm -rf node_modules package-lock.json
npm install
```
