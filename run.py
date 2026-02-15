#!/usr/bin/env python3
"""
Entry point - run from project root.
Usage: python run.py [--encrypt]
       python run.py --pdf
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def main():
    if "--pdf" in sys.argv:
        script = "src/generate_submission_pdf.py"
        args = [a for a in sys.argv[1:] if a != "--pdf"]
    else:
        script = "src/main.py"
        args = sys.argv[1:]
    subprocess.run([sys.executable, script] + args, cwd=PROJECT_ROOT, check=True)


if __name__ == "__main__":
    main()
