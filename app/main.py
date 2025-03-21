import os
import sys
from pathlib import Path
import uvicorn

# Add the project root directory to Python path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.api import app

if __name__ == "__main__":
    # Create and run the uvicorn server properly
    uvicorn.run(app, host="0.0.0.0", port=8000)