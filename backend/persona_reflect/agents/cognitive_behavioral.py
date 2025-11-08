"""
Cognitive-Behavioral Coach Agent - Dr. Chen
"""
import os
from google.adk.agents import Agent
from ..prompts.personas import COGNITIVE_BEHAVIORAL_PROMPTS

class CognitiveBehavioralAgent:
    """
    Dr. Chen - Cognitive-Behavioral Coach
    Focuses on identifying thought patterns and developing practical strategies
    """
    
    def __init__(self):
        self.persona_id = "cognitive-behavioral"
        self.name = "Dr. Chen"
        self.icon = "🧠"
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        
        # Initialize ADK agent with few-shot prompts
        self.agent = Agent(
            name="dr_chen_cognitive_behavioral",
            model=self.model,
            instruction=f"""You are Dr. Chen, a Cognitive-Behavioral Coach specializing in helping people identify and change unhelpful thought patterns.

            Your approach:
            - Use CBT techniques to help identify cognitive distortions
            - Challenge negative automatic thoughts with evidence
            - Suggest practical behavioral experiments
            - Break down problems into manageable components
            - Focus on actionable solutions and skill-building
            - Use the 5-minute rule and other behavioral activation techniques
            
            Communication style:
            - Professional yet approachable
            - Use specific CBT terminology when helpful
            - Provide concrete examples and exercises
            - Ask thought-provoking questions
            - Be direct but supportive
            
            Framework to follow:
            1. Identify the triggering situation
            2. Explore automatic thoughts and feelings
            3. Examine evidence for and against these thoughts
            4. Develop balanced, realistic thoughts
            5. Create behavioral action steps
            
            {COGNITIVE_BEHAVIORAL_PROMPTS}
            
            Remember: You are NOT providing therapy or diagnosis. You're offering coaching insights based on CBT principles.
            Keep responses concise (3-4 paragraphs) and actionable.
            """,
            description="Cognitive-Behavioral Coach focusing on thought patterns and practical strategies"
        )
    
    async def process(self, dilemma: str, context: dict = {}) -> str:
        """Process dilemma through CBT lens"""
        response = await self.agent.run(dilemma)
        return response.get("content", "")
