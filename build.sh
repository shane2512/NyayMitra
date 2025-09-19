#!/bin/bash
# Build script for Vercel deployment

echo "Building NyayMitra frontend..."

# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build the React app
npm run build

echo "Frontend build completed!"
