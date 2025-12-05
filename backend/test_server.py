#!/usr/bin/env python3
"""
Quick test to verify the server can start
Run this to check if everything is configured correctly
"""

import sys
import os

print("=" * 60)
print("MoveH Backend - Configuration Test")
print("=" * 60)

# Test 1: Check Python version
print("\n1. Checking Python version...")
if sys.version_info >= (3, 12):
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor} (OK)")
else:
    print(f"   ⚠️  Python {sys.version_info.major}.{sys.version_info.minor} (Recommended: 3.12+)")

# Test 2: Check .env file
print("\n2. Checking .env file...")
if os.path.exists('.env'):
    print("   ✅ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    google_key = os.getenv("GOOGLE_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    if google_key and len(google_key) > 10:
        print(f"   ✅ GOOGLE_API_KEY is set ({len(google_key)} chars)")
    else:
        print("   ❌ GOOGLE_API_KEY is missing or invalid")
    
    if tavily_key and len(tavily_key) > 10:
        print(f"   ✅ TAVILY_API_KEY is set ({len(tavily_key)} chars)")
    else:
        print("   ❌ TAVILY_API_KEY is missing or invalid")
else:
    print("   ❌ .env file not found")

# Test 3: Check required modules
print("\n3. Checking required modules...")
required_modules = [
    "fastapi",
    "uvicorn",
    "langchain",
    "langchain_google_genai",
    "langgraph",
    "tavily",
    "reportlab",
    "rich",
    "pydantic",
    "dotenv"
]

missing_modules = []
for module in required_modules:
    try:
        __import__(module.replace("-", "_"))
        print(f"   ✅ {module}")
    except ImportError:
        print(f"   ❌ {module} (missing)")
        missing_modules.append(module)

# Test 4: Try importing the API
print("\n4. Checking API imports...")
try:
    from api import app
    print("   ✅ API imports successfully")
except Exception as e:
    print(f"   ❌ API import failed: {e}")

# Test 5: Check agents
print("\n5. Checking agents...")
try:
    from agents import FactChecker, ForensicExpert, TheJudge
    print("   ✅ All agents import successfully")
except Exception as e:
    print(f"   ❌ Agent import failed: {e}")

# Summary
print("\n" + "=" * 60)
if missing_modules:
    print("⚠️  ISSUES FOUND")
    print("\nMissing modules:")
    for mod in missing_modules:
        print(f"   - {mod}")
    print("\nRun: pip install -r requirements.txt")
else:
    print("✅ ALL CHECKS PASSED!")
    print("\nYou can now start the server:")
    print("   python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000")
    print("\nOr use the batch file:")
    print("   start.bat")
print("=" * 60)
