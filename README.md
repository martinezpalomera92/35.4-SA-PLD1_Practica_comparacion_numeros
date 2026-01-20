# LocalAI Agent

A fully functional, offline-capable AI agent built with React and Electron. This application uses [Transformers.js](https://xenova.github.io/transformers.js/) to run machine learning models directly in your browser or desktop environment without requiring a Python backend.

## Features

- **100% Local Processing**: No data ever leaves your computer.
- **Offline First**: Works without an internet connection once the model is downloaded.
- **React-powered UI**: Modern, responsive interface with Tailwind CSS.
- **Electron Desktop Wrapper**: Can be installed as a native application on Windows, macOS, or Linux.

## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or higher)
- [npm](https://www.npmjs.com/)

## Getting Started

### 1. Clone the repository and install dependencies

```bash
npm install
```

### 2. Download the Model for Offline Use

The app requires a model to function. By default, it will attempt to download the model from Hugging Face on the first run. For a truly offline experience, you can pre-download the model into the `public/models` directory.

You can run the provided download script (Note: Requires internet for this step):

```bash
node download_model.js
```

### 3. Run the application in development mode

```bash
npm run electron:dev
```

### 4. Build and Package for Production

To create a distributable installer for your operating system:

```bash
npm run electron:build
```

The packaged application will be available in the `release/` directory.

## Technical Architecture

- **Frontend**: React.js with Vite
- **Styling**: Tailwind CSS 4
- **AI Engine**: @xenova/transformers (Transformers.js)
- **Background Processing**: Web Workers (ensures UI doesn't freeze during inference)
- **Desktop Wrapper**: Electron

## License

MIT
