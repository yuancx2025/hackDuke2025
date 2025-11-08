#!/usr/bin/env python3
"""
🚀 Quick Test Script for PersonaReflect Backend
================================================
Minimal script to test if the backend agents work
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def test_step(step_num, total, description):
    """Print test step"""
    print(f"\n{BLUE}[{step_num}/{total}] {description}...{RESET}")

def success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

async def test_agents():
    """Test the actual agent orchestrator"""
    print(f"{BLUE}🧪 Testing Agent Orchestrator...{RESET}\n")
    
    try:
        from persona_reflect.agents.orchestrator import PersonaReflectOrchestrator
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Initialize
        print("⏳ Initializing orchestrator...")
        orchestrator = PersonaReflectOrchestrator()
        success("Orchestrator initialized")
        
        # Test with simple dilemma
        test_dilemma = "I'm feeling overwhelmed with too many tasks."
        print(f"\n📝 Test dilemma: {test_dilemma}")
        print("⏳ Processing through all 4 personas (10-20 seconds)...\n")
        
        result = await orchestrator.process_dilemma(
            user_id="test_user",
            dilemma=test_dilemma,
            context={}
        )
        
        success("All personas responded!")
        print()
        
        for response in result["responses"]:
            print(f"{response['icon']} {response['name']}:")
            print(f"   {response['response'][:80]}...")
            print()
        
        if result.get("suggested_actions"):
            success(f"Generated {len(result['suggested_actions'])} action items")
        
        print(f"\n{GREEN}{'='*60}")
        print("  🎉 BACKEND FULLY FUNCTIONAL!")
        print(f"{'='*60}{RESET}\n")
        
        return True
        
    except Exception as e:
        error(f"Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print(f"\n{BLUE}{'='*60}")
    print("  PersonaReflect - Quick Smoke Test")
    print(f"{'='*60}{RESET}\n")
    
    total_tests = 5
    passed = 0
    
    # Test 1: .env file
    test_step(1, total_tests, "Checking .env configuration")
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        error(".env file not found!")
        print(f"  Run: cp .env.example .env")
        print(f"  Then edit .env and add your GOOGLE_API_KEY")
    else:
        success(".env file exists")
        
        # Check API key
        with open(env_file) as f:
            content = f.read()
            if "your_google_ai_api_key_here" in content:
                error("GOOGLE_API_KEY not configured!")
                print(f"  Edit backend/.env and replace with your actual API key")
                print(f"  Get key from: https://aistudio.google.com/app/apikey")
            else:
                success("GOOGLE_API_KEY appears to be set")
                passed += 1
    
    # Test 2: Required packages
    test_step(2, total_tests, "Checking Python packages")
    required = ["google.adk", "fastapi", "uvicorn", "pydantic", "dotenv"]
    missing = []
    all_installed = True
    
    for pkg in required:
        try:
            if pkg == "dotenv":
                __import__("dotenv")
            else:
                __import__(pkg)
            success(f"{pkg} installed")
        except ImportError:
            missing.append(pkg)
            error(f"{pkg} NOT installed")
            all_installed = False

    if all_installed:
        passed += 1
    else:
        print(f"\n  Install with: pip install -r requirements.txt")
    
    # Test 3: Project structure
    test_step(3, total_tests, "Checking project structure")
    required_files = [
        "persona_reflect/__init__.py",
        "persona_reflect/main.py",
        "persona_reflect/agents/orchestrator.py",
        "persona_reflect/agents/cognitive_behavioral.py",
        "persona_reflect/agents/empathetic_friend.py",
        "persona_reflect/agents/rational_analyst.py",
        "persona_reflect/agents/mindfulness_mentor.py",
        "persona_reflect/prompts/personas.py",
        "persona_reflect/tools/calendar_tools.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = Path(__file__).parent / file_path
        if full_path.exists():
            success(f"{file_path}")
        else:
            error(f"{file_path} MISSING")
            all_exist = False
    
    if all_exist:
        passed += 1
    
    # Test 4: Import agents
    test_step(4, total_tests, "Testing agent imports")
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from persona_reflect.agents.orchestrator import PersonaReflectOrchestrator
        success("PersonaReflectOrchestrator imported")
        
        from persona_reflect.tools.calendar_tools import CalendarTool
        success("CalendarTool imported")
        
        passed += 1
    except ImportError as e:
        error(f"Import failed: {e}")
    
    # Test 5: Environment variables
    test_step(5, total_tests, "Checking environment variables")
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GOOGLE_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        
        if api_key and api_key != "your_google_ai_api_key_here":
            success(f"GOOGLE_API_KEY configured")
            success(f"Using model: {model}")
            passed += 1
        else:
            error("GOOGLE_API_KEY not properly set")
    except Exception as e:
        error(f"Environment check failed: {e}")
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"Results: {passed}/{total_tests} tests passed")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    if passed == total_tests:
        print(f"{GREEN}✓ All checks passed! Ready to test the agents.{RESET}")
        
        # Ask if user wants to run live test
        try:
            response = input(f"\n{YELLOW}Would you like to run a live agent test? (y/n): {RESET}").strip().lower()
            if response == 'y':
                print(f"\n{BLUE}Running live agent test...{RESET}\n")
                agents_ok = asyncio.run(test_agents())
                if agents_ok:
                    return 0
                else:
                    return 1
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Skipped live test{RESET}\n")
        
        print(f"\nNext steps:")
        print(f"  1. Run interactive demo: python interactive_demo.py")
        print(f"  2. Start server: uvicorn persona_reflect.main:app --reload")
        print(f"  3. View API docs: http://localhost:8000/docs\n")
        return 0
    else:
        print(f"{YELLOW}⚠ {total_tests - passed} checks failed. Fix issues above.{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
