# Frontend - Text Adventure Game

## Features

- **Interactive UI**: Engaging interface for playing the text adventure game.
- **Next.js framework**: Optimized for performance and SEO.
- **React and TypeScript**: Component-based development with type safety.
- **Tailwind CSS**: Modern styling framework for UI customization.

## Tech Stack

- **Next.js**: React framework for server-side rendering and static site generation.
- **React**: Component-based UI library.
- **TypeScript**: Enhances maintainability and type safety.
- **Tailwind CSS**: Utility-first styling framework.

## Installation

### Prerequisites

- Node.js 16+

### Setup

1. Clone the repository:

   ```sh


   ```

2. Install dependencies:
   ```sh
   yarn install
   ```
3. Start the development server:
   ```sh
   yarn run dev
   ```

## Configuration

The frontend communicates with the backend API at:

```sh
http://127.0.0.1:8000/play/
```

Ensure the backend is running before starting the frontend.

## Available Scripts

| Command         | Description                           |
| --------------- | ------------------------------------- |
| `npm run dev`   | Runs the app in development mode.     |
| `npm run build` | Builds the app for production.        |
| `npm run start` | Starts the production server.         |
| `npm run lint`  | Runs ESLint to check for code issues. |

## How It Works

1. The frontend sends user input to the backend.
2. The backend generates the next game response using OpenAI.
3. The UI updates with the new game narrative and options.
