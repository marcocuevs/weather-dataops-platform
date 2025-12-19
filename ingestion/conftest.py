# =============================================================================
# Pytest Configuration
# Adds src/ to Python path so tests can import modules correctly
# =============================================================================

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
