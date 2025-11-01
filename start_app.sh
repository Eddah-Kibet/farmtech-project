#!/bin/bash

echo "🚀 Starting Farm Produce Marketplace"
echo "===================================="

# Check if backend dependencies are installed
if [ ! -d "server/instance" ]; then
    echo "📁 Creating instance directory..."
    mkdir -p server/instance
fi

# Start backend
echo "🔧 Starting Flask backend..."
cd server
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:5000/ > /dev/null; then
    echo "✅ Backend is running on http://localhost:5000"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🎨 Starting React frontend..."
cd client
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Application started successfully!"
echo ""
echo "📋 Access URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:5000"
echo ""
echo "🔑 Test Credentials:"
echo "   Farmer: jesse@example.com / password123"
echo "   Buyer:  buyer@example.com / password123"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait