# Frontend Development Guide

## Overview

Next.js 14 frontnd for AI Resume Analyzer with Tailwind CSS and TypeScript.

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx              # Home page
│   ├── upload/
│   │   └── page.tsx          # Resume upload page
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Pages

### Home Page (`/`)

- Displays "Resume Analyzer" title
- Shows platform description
- "Start Analysis" button links to `/upload`

**File**: `app/page.tsx`

### Upload Page (`/upload`)

- File input for PDF/DOCX files
- Shows selected file name
- Upload button with loading state
- Displays analysis results:
  - Score (with progress bar)
  - Skills found (green badges)
  - Missing skills (orange badges)
- Error handling for invalid files

**File**: `app/upload/page.tsx`

**Features**:
- Client-side component (uses `'use client'`)
- File type validation
- Loading state management
- Result state management
- Error state management
- Responsive design with Tailwind CSS

## API Integration

### File Upload Flow

1. **User selects file**
   - Validation: accepts only `.pdf` and `.docx`
   - Type checking: `application/pdf` and Word document types

2. **Form submission**
   - Creates FormData with file
   - POSTs to `http://localhost:8000/analyze`
   - Sets loading state

3. **Response handling**
   - Parses JSON response
   - Displays results in card format
   - Shows error message if request fails

4. **Reset option**
   - Button to analyze another resume
   - Clears results and file state

### API Endpoint

```
POST http://localhost:8000/analyze
Content-Type: multipart/form-data

Field: file (File)

Response:
{
  "score": 75,
  "skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"]
}
```

## Styling

### Tailwind CSS

All styling uses Tailwind utility classes:
- Color scheme: Blue/Indigo theme
- Responsive: Mobile-first approach
- Components:
  - Gradient backgrounds
  - Rounded cards with shadows
  - Colored badges for skills
  - Progress bar for score
  - Disabled states for buttons

### Custom CSS

Global styles in `app/globals.css`:
- Tailwind directives
- Smooth scroll behavior

## State Management

Upload page uses React hooks:
- `useState` for file, loading, result, error states
- No external state management library

## Error Handling

- File type validation (PDF/DOCX only)
- File size validation (if exceeded server-side)
- Network error handling
- User-friendly error messages

## Development

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Open `http://localhost:3000` in browser.

### Build for Production

```bash
npm run build
npm start
```

### Linting

```bash
npm run lint
```

## Next Steps

- [ ] Add loading skeleton
- [ ] Add file drag-and-drop
- [ ] Add result sharing/export
- [ ] Add history of analyses
- [ ] Implement dark mode
- [ ] Add accessibility improvements
- [ ] Add unit and integration tests
