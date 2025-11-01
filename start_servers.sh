#!/bin/bash

# Farm Produce Marketplace - Server Startup Script

echo "🚀 Starting Farm Produce Marketplace..."

# Function to kill background processes on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend server
echo "📡 Starting Flask backend server..."
cd server
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🌐 Starting React frontend server..."
cd ../client
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Servers started successfully!"
echo "📡 Backend API: http://localhost:5000"
echo "🌐 Frontend App: http://localhost:5173"
echo ""
echo "Test Credentials:"
echo "   Farmer: jesse@example.com / password123"
echo "   Buyer:  buyer@example.com / password123"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for background processes
wait