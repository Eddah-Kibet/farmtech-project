# Farm Produce Marketplace

A full-stack marketplace connecting farmers with buyers for fresh produce.

## Features

- **For Farmers**: List products, manage inventory, receive orders, get ratings
- **For Buyers**: Browse products, add to cart, place orders, rate farmers
- **Real-time messaging** between farmers and buyers
- **Leaderboard** system for top-rated farmers
- **Dark/Light theme** support

## Quick Start

### Backend (Flask)
```bash
cd server
pip install -r requirements.txt
python app.py
```
Server runs on: http://localhost:5000

### Frontend (React + Vite)
```bash
cd client
npm install
npm run dev
```
Client runs on: http://localhost:5173

## Tech Stack

- **Backend**: Flask, SQLAlchemy, JWT Authentication
- **Frontend**: React, Vite, Tailwind CSS
- **Database**: SQLite
- **Styling**: Tailwind CSS + Custom CSS

## Project Structure

```
├── server/          # Flask backend
│   ├── app.py       # Main application
│   ├── models.py    # Database models
│   └── routes/      # API routes
├── client/          # React frontend
│   ├── src/
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Page components
│   │   └── context/     # React contexts
│   └── public/      # Static assets
```

## Default Users

Create accounts through the registration page or use the seeded data if available.