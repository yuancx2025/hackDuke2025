#!/usr/bin/env python3
"""
🎭 PersonaReflect Interactive Demo
===================================
Live demonstration of the multi-agent AI coaching system
"""

import asyncio
import sys
import os
from typing import Dict, Any
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona_reflect.agents.orchestrator import PersonaReflectOrchestrator
from dotenv import load_dotenv

# Load environment
load_dotenv()

# ANSI color codes for pretty terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print a fancy header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_persona(icon: str, name: str, response: str):
    """Print a persona response with nice formatting"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{icon} {name}:{Colors.END}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}")
    print(f"{response}")
    print(f"{Colors.BLUE}{'─'*60}{Colors.END}\n")

def print_actions(actions: list):
    """Print suggested actions"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}✨ Suggested Actions:{Colors.END}")
    for i, action in enumerate(actions, 1):
        print(f"{Colors.GREEN}  {i}. {action}{Colors.END}")
    print()

def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}{Colors.BOLD}❌ Error: {message}{Colors.END}")

def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}{Colors.BOLD}✅ {message}{Colors.END}")

# Sample dilemmas for quick demo
SAMPLE_DILEMMAS = [
    {
        "title": "Career Decision",
        "dilemma": "I've been offered a promotion that would mean more money and prestige, but also longer hours and more stress. I'm torn between career advancement and my current work-life balance.",
        "context": {"current_job_satisfaction": "7/10", "family_time_priority": "high"}
    },
    {
        "title": "Procrastination Pattern",
        "dilemma": "I keep putting off starting my important personal project. Every day I tell myself I'll begin, but then I find excuses and distractions. It's been months now.",
        "context": {"project_type": "creative", "deadline": "self-imposed"}
    },
    {
        "title": "Social Anxiety",
        "dilemma": "I want to be more social and make new friends, but I get anxious in social situations and often bail on plans at the last minute. This is affecting my relationships.",
        "context": {"age_group": "mid-20s", "past_experiences": "some negative"}
    },
    {
        "title": "Self-Doubt",
        "dilemma": "Despite having good accomplishments, I constantly feel like I'm not good enough and worry that people will discover I'm a fraud. This impostor syndrome is exhausting.",
        "context": {"field": "tech/creative", "experience_level": "mid-career"}
    }
]

class InteractiveDemo:
    """Interactive demo orchestrator"""
    
    def __init__(self):
        self.orchestrator = None
        self.session_history = []
    
    async def initialize(self):
        """Initialize the orchestrator"""
        print_header("🎭 PersonaReflect Demo Initializing...")
        print(f"{Colors.YELLOW}⏳ Loading AI agents...{Colors.END}")
        
        try:
            self.orchestrator = PersonaReflectOrchestrator()
            print_success("All 4 AI personas loaded successfully!")
            await asyncio.sleep(1)
            return True
        except Exception as e:
            print_error(f"Failed to initialize: {str(e)}")
            print(f"\n{Colors.YELLOW}💡 Make sure you have:{Colors.END}")
            print(f"   1. Set GOOGLE_API_KEY in your .env file")
            print(f"   2. Installed all requirements: pip install -r requirements.txt")
            print(f"   3. Valid Google AI API key with Gemini access")
            return False
    
    def show_welcome(self):
        """Show welcome screen"""
        print_header("🎭 PersonaReflect - Multi-Agent AI Coach")
        print(f"{Colors.CYAN}Welcome to PersonaReflect!{Colors.END}")
        print(f"\nGet insights from 4 specialized AI personas:")
        print(f"  🧠 {Colors.BOLD}Dr. Chen{Colors.END} - Cognitive-Behavioral Coach")
        print(f"  💙 {Colors.BOLD}Maya{Colors.END} - Empathetic Friend")
        print(f"  📊 {Colors.BOLD}Alex{Colors.END} - Rational Analyst")
        print(f"  🧘 {Colors.BOLD}Sage{Colors.END} - Mindfulness Mentor")
        print()
    
    def show_menu(self):
        """Show main menu"""
        print(f"\n{Colors.BOLD}What would you like to do?{Colors.END}")
        print(f"  1. Try a sample dilemma (quick demo)")
        print(f"  2. Enter your own dilemma")
        print(f"  3. View session history")
        print(f"  4. Exit")
        print()
    
    def show_sample_dilemmas(self):
        """Show sample dilemmas menu"""
        print(f"\n{Colors.BOLD}Sample Dilemmas:{Colors.END}")
        for i, sample in enumerate(SAMPLE_DILEMMAS, 1):
            print(f"  {i}. {Colors.BOLD}{sample['title']}{Colors.END}")
            print(f"     {Colors.CYAN}{sample['dilemma'][:80]}...{Colors.END}")
        print(f"  0. Back to main menu")
        print()
    
    async def process_dilemma(self, dilemma: str, context: Dict[str, Any] = {}):
        """Process a dilemma through all personas"""
        print_header("🎭 Processing Your Dilemma")
        
        print(f"{Colors.YELLOW}📝 Your dilemma:{Colors.END}")
        print(f"{Colors.CYAN}{dilemma}{Colors.END}\n")
        
        if context:
            print(f"{Colors.YELLOW}📋 Context: {json.dumps(context, indent=2)}{Colors.END}\n")
        
        print(f"{Colors.YELLOW}⏳ Consulting all 4 AI personas (this may take 10-20 seconds)...{Colors.END}\n")
        
        try:
            # Process through orchestrator
            result = await self.orchestrator.process_dilemma(
                user_id="demo_user",
                dilemma=dilemma,
                context=context
            )
            
            # Display each persona's response
            print_header("🎭 Persona Insights")
            for response in result["responses"]:
                print_persona(
                    response["icon"],
                    response["name"],
                    response["response"]
                )
                await asyncio.sleep(0.5)  # Dramatic pause
            
            # Display suggested actions
            if result.get("suggested_actions"):
                print_actions(result["suggested_actions"])
            
            # Save to history
            self.session_history.append({
                "timestamp": datetime.now().isoformat(),
                "dilemma": dilemma,
                "result": result
            })
            
            print_success("Reflection complete!")
            
        except Exception as e:
            print_error(f"Failed to process dilemma: {str(e)}")
            import traceback
            print(f"{Colors.RED}{traceback.format_exc()}{Colors.END}")
    
    async def run(self):
        """Main demo loop"""
        # Initialize
        if not await self.initialize():
            return
        
        self.show_welcome()
        
        while True:
            self.show_menu()
            
            try:
                choice = input(f"{Colors.BOLD}Enter your choice (1-4): {Colors.END}").strip()
                
                if choice == "1":
                    # Sample dilemma
                    self.show_sample_dilemmas()
                    sample_choice = input(f"{Colors.BOLD}Choose a sample (0-{len(SAMPLE_DILEMMAS)}): {Colors.END}").strip()
                    
                    if sample_choice == "0":
                        continue
                    
                    try:
                        idx = int(sample_choice) - 1
                        if 0 <= idx < len(SAMPLE_DILEMMAS):
                            sample = SAMPLE_DILEMMAS[idx]
                            await self.process_dilemma(
                                sample["dilemma"],
                                sample.get("context", {})
                            )
                        else:
                            print_error("Invalid choice")
                    except ValueError:
                        print_error("Please enter a number")
                
                elif choice == "2":
                    # Custom dilemma
                    print(f"\n{Colors.BOLD}Enter your dilemma:{Colors.END}")
                    print(f"{Colors.CYAN}(Press Enter twice when done){Colors.END}\n")
                    
                    lines = []
                    empty_count = 0
                    while empty_count < 1:
                        line = input()
                        if line.strip():
                            lines.append(line)
                            empty_count = 0
                        else:
                            empty_count += 1
                    
                    dilemma = " ".join(lines).strip()
                    
                    if dilemma:
                        await self.process_dilemma(dilemma)
                    else:
                        print_error("No dilemma entered")
                
                elif choice == "3":
                    # View history
                    if not self.session_history:
                        print(f"\n{Colors.YELLOW}No session history yet.{Colors.END}")
                    else:
                        print_header("📜 Session History")
                        for i, entry in enumerate(self.session_history, 1):
                            print(f"{Colors.BOLD}{i}. {entry['timestamp']}{Colors.END}")
                            print(f"   {Colors.CYAN}{entry['dilemma'][:100]}...{Colors.END}\n")
                
                elif choice == "4":
                    # Exit
                    print_header("👋 Thank You!")
                    print(f"{Colors.CYAN}Thanks for trying PersonaReflect!{Colors.END}")
                    print(f"{Colors.YELLOW}✨ Your personal board of advisors, powered by AI{Colors.END}\n")
                    break
                
                else:
                    print_error("Invalid choice. Please enter 1-4")
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Demo interrupted. Goodbye!{Colors.END}\n")
                break
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}")
                import traceback
                print(f"{Colors.RED}{traceback.format_exc()}{Colors.END}")

async def main():
    """Entry point"""
    demo = InteractiveDemo()
    await demo.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Goodbye!{Colors.END}\n")
        sys.exit(0)
