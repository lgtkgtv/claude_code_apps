#!/bin/bash

echo "🚀 Setting up Expense Tracker Application..."

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ uv is required but not installed"
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv found: $(uv --version)"

# Install dependencies using uv
echo "📥 Installing dependencies with uv..."
uv sync

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  uv run python main.py"
echo ""
echo "The application will be available at: http://localhost:8080"