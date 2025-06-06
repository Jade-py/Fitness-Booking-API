
echo "🚀 Setting up FastAPI Fitness Booking API..."

# Step 1: Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 2: Install dependencies
echo "📥 Installing dependencies..."
pip install install -r requirements.txt

# Step 3: Seed the database
echo "🌱 Seeding database..."
python -m app.seed

# Step 4: Run the server
echo "🚀 Running server on http://127.0.0.1:8000 ..."
uvicorn app.main:app --reload