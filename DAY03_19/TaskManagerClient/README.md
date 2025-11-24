# TaskManager Client

A React 18 frontend application for the TaskManager API, built with Vite for fast development and production builds.

## Project Structure

```
TaskManagerClient/
├── eslint.config.js
├── index.html
├── package.json
├── pnpm-lock.yaml
├── README.md
├── vite.config.js
└── src/
    ├── App.css
    ├── App.jsx
    ├── Layouts/
    │   ├── MainLayout.jsx
    │   └── NoLayout.jsx
    ├── assets/
    │   └── react.svg
    ├── components/
    │   ├── Footer.jsx
    │   ├── Hero.jsx
    │   ├── NavBar.jsx
    │   ├── TaskForm.jsx
    │   └── TaskList.jsx
    ├── index.css
    ├── main.jsx
    └── pages/
        ├── Dashboard.jsx
        ├── Error.jsx
        ├── Home.jsx
        ├── Login.jsx
        ├── Register.jsx
        └── Tasks.jsx
```

## Tech Stack

- **Frontend**: React 18, Vite, React Router
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **API Integration**: Axios

## Prerequisites

- Node.js (v16 or higher)
- npm or pnpm

## Setup Instructions

1. **Navigate to the Client Directory**:
   ```bash
   cd DAY03_19/TaskManagerClient
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Environment Configuration** (Optional):
   - Create a `.env` file in the root directory if needed for API URL.
   - Example:
     ```
     VITE_API_BASE_URL=http://localhost:8000/api/v1
     ```

4. **Run the Development Server**:
   ```bash
   npm run dev
   # or
   pnpm run dev
   ```
   - Open [http://localhost:5173](http://localhost:5173) in your browser.

5. **Build for Production**:
   ```bash
   npm run build
   # or
   pnpm run build
   ```

6. **Preview Production Build**:
   ```bash
   npm run preview
   # or
   pnpm run preview
   ```

## Routes

- `/` - Home page
- `/login` - User login
- `/register` - User registration
- `/dashboard` - User dashboard
- `/tasks` - Task management

## Components

- **NavBar**: Navigation bar
- **Footer**: Footer component
- **Hero**: Hero section
- **TaskForm**: Form for creating/editing tasks
- **TaskList**: List of tasks

## Pages

- **Home**: Landing page
- **Login**: Authentication page
- **Register**: User registration
- **Dashboard**: User dashboard
- **Tasks**: Task management page
- **Error**: Error page

## Layouts

- **MainLayout**: Layout with NavBar and Footer
- **NoLayout**: Layout without NavBar and Footer (for auth pages)
