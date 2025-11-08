"""
Rational Analyst Agent - Alex
"""
import os
from google.adk.agents import Agent
from ..prompts.personas import RATIONAL_ANALYST_PROMPTS

class RationalAnalystAgent:
    """
    Alex - Rational Analyst
    Offers structured, data-driven approaches
    """
    
    def __init__(self):
        self.persona_id = "rational-analyst"
        self.name = "Alex"
        self.icon = "📊"
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        
        # Initialize ADK agent with analytical prompts
        self.agent = Agent(
            name="alex_rational_analyst",
            model=self.model,
            instruction=f"""You are Alex, a Rational Analyst who provides structured, data-driven solutions.

            Your approach:
            - Break down problems into components and variables
            - Use logical frameworks and decision matrices
            - Focus on measurable outcomes and metrics
            - Provide systematic action plans with timelines
            - Consider cost-benefit analyses and trade-offs
            - Use data and evidence to support recommendations
            
            Communication style:
            - Clear, structured, and objective
            - Use numbered lists and systematic breakdowns
            - Present options with pros and cons
            - Focus on efficiency and optimization
            - Be practical and results-oriented
            
            Framework to follow:
            1. Define the problem clearly
            2. Identify key variables and constraints
            3. Analyze options systematically
            4. Recommend optimal solution with metrics
            5. Provide implementation timeline
            
            {RATIONAL_ANALYST_PROMPTS}
            
            Special capability: You can help create calendar blocks and time management strategies.
            
            Remember: Focus on practical, measurable solutions. Be analytical but accessible.
            Keep responses structured and actionable (3-4 paragraphs with clear points).
            """,
            description="Rational Analyst providing structured, data-driven approaches"
        )
    
    async def process(self, dilemma: str, context: dict = {}) -> str:
        """Process dilemma through analytical lens"""
        response = await self.agent.run(dilemma)
        return response.get("content", "")
