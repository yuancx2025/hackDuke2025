"""
Orchestrator Agent - Coordinates the four persona agents
"""
import asyncio
from typing import List, Dict, Any
from datetime import datetime
import os
import uuid

from google.adk import Runner
from google.adk.agents import Agent, ParallelAgent
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types as genai_types

from .cognitive_behavioral import CognitiveBehavioralAgent
from .empathetic_friend import EmpatheticFriendAgent
from .rational_analyst import RationalAnalystAgent
from .mindfulness_mentor import MindfulnessMentorAgent

class PersonaReflectOrchestrator:
    """
    Main orchestrator that coordinates all persona agents
    """
    
    def __init__(self):
        """Initialize the orchestrator with all persona agents"""
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        
        # Initialize persona agents
        self.cognitive_agent = CognitiveBehavioralAgent()
        self.empathetic_agent = EmpatheticFriendAgent()
        self.rational_agent = RationalAnalystAgent()
        self.mindfulness_agent = MindfulnessMentorAgent()
        
        # Create parallel agent for concurrent persona processing
        self.parallel_processor = ParallelAgent(
            name="persona_parallel_processor",
            sub_agents=[
                self.cognitive_agent.agent,
                self.empathetic_agent.agent,
                self.rational_agent.agent,
                self.mindfulness_agent.agent,
            ]
        )
        
        # Create main orchestrator agent
        self.orchestrator = Agent(
            name="persona_reflect_orchestrator",
            model=self.model,
            instruction="""You are the PersonaReflect Orchestrator.
            
            Your role is to:
            1. Receive user dilemmas and coordinate responses from four specialized AI coaches
            2. Ensure each persona provides unique, valuable insights
            3. Synthesize insights into coherent action plans when requested
            4. Maintain conversation context and user history
            
            Remember:
            - Each persona should maintain their distinct voice and approach
            - Responses should be empathetic, actionable, and non-judgmental
            - Focus on empowering users to find their own solutions
            """,
            description="Orchestrates multi-persona self-reflection coaching"
        )
    
    async def process_dilemma(
        self,
        user_id: str,
        dilemma: str,
        context: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Process a user's dilemma through all persona agents
        """
        print(f"🎭 Orchestrator processing dilemma for user: {user_id}")
        
        # Prepare the message for all personas
        prompt = f"""
        User Dilemma: {dilemma}
        
        Context: {context if context else 'No additional context provided'}
        
        Please provide your unique perspective and guidance for this dilemma.
        """
        
        # Process through all personas in parallel
        tasks = [
            self._get_persona_response(self.cognitive_agent, prompt),
            self._get_persona_response(self.empathetic_agent, prompt),
            self._get_persona_response(self.rational_agent, prompt),
            self._get_persona_response(self.mindfulness_agent, prompt)
        ]
        
        responses = await asyncio.gather(*tasks)
        
        # Extract suggested actions from responses
        suggested_actions = await self._synthesize_actions(responses, dilemma)
        
        return {
            "id": f"entry-{datetime.now().timestamp()}",
            "responses": responses,
            "suggested_actions": suggested_actions
        }

    async def _invoke_agent(
        self,
        agent: Agent,
        session_prefix: str,
        prompt: str,
        user_id: str = "persona_reflect",
    ) -> str:
        """Execute an ADK agent with a single-turn prompt."""
        runner = Runner(
            agent=agent,
            app_name="persona_reflect",
            session_service=InMemorySessionService(),
        )
        session_id = f"{session_prefix}-{uuid.uuid4()}"
        message = genai_types.Content(
            role="user",
            parts=[genai_types.Part(text=prompt)]
        )
        response_text = ""

        try:
            await runner.session_service.create_session(
                app_name="persona_reflect",
                user_id=user_id,
                session_id=session_id,
            )

            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message,
            ):
                if event.author == "user":
                    continue
                if event.content and event.content.parts:
                    text_fragments = [
                        part.text or ""
                        for part in event.content.parts
                        if getattr(part, "text", None)
                    ]
                    if text_fragments:
                        response_text = "".join(text_fragments).strip()

                if getattr(event, "is_final_response", None) and event.is_final_response():
                    break
        finally:
            await runner.close()

        return response_text
    
    async def _get_persona_response(
        self,
        persona_agent,
        prompt: str
    ) -> Dict[str, str]:
        """
        Get response from a specific persona agent
        """
        try:
            response_text = await self._invoke_agent(
                persona_agent.agent,
                session_prefix=persona_agent.persona_id,
                prompt=prompt,
                user_id="demo_user",
            )
        except Exception as e:
            print(f"❌ Error getting response from {persona_agent.name}: {str(e)}")
            response_text = ""

        if not response_text:
            response_text = "I'm having trouble processing this right now. Please try again."

        return {
            "persona": persona_agent.persona_id,
            "name": persona_agent.name,
            "icon": persona_agent.icon,
            "response": response_text
        }
    
    async def _synthesize_actions(
        self,
        responses: List[Dict[str, str]],
        dilemma: str
    ) -> List[str]:
        """
        Synthesize responses into suggested action steps
        """
        synthesis_prompt = f"""
        Based on the following diverse perspectives on this dilemma:
        
        Dilemma: {dilemma}
        
        Perspectives:
        {self._format_responses(responses)}
        
        Please synthesize these insights into 3-5 concrete, actionable steps.
        Focus on practical actions the user can take immediately.
        Return only the action steps as a numbered list.
        """
        
        try:
            result_text = await self._invoke_agent(
                self.orchestrator,
                session_prefix="orchestrator-synthesis",
                prompt=synthesis_prompt,
            )
            actions = result_text.strip().split("\n")
            # Clean up the actions
            actions = [
                action.strip().lstrip("0123456789. ")
                for action in actions
                if action.strip()
            ]
            return actions[:5]  # Limit to 5 actions
        except Exception as e:
            print(f"❌ Error synthesizing actions: {str(e)}")
            return []
    
    def _format_responses(self, responses: List[Dict[str, str]]) -> str:
        """Format responses for synthesis"""
        formatted = []
        for resp in responses:
            formatted.append(f"{resp['name']} ({resp['persona']}): {resp['response']}")
        return "\n\n".join(formatted)
    
    async def create_action_plan(
        self,
        entry_id: str,
        responses: List[Dict[str, Any]],
        preferences: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        Create a comprehensive action plan from persona responses
        """
        plan_prompt = f"""
        Create a detailed action plan based on these coaching perspectives:
        
        {self._format_responses(responses)}
        
        User preferences: {preferences if preferences else 'None specified'}
        
        Generate 5-7 specific, measurable action steps that:
        1. Are immediately actionable
        2. Build on each other progressively
        3. Address the core issues identified
        4. Can be tracked and measured
        
        Return only the action steps as a numbered list.
        """
        
        try:
            result_text = await self._invoke_agent(
                self.orchestrator,
                session_prefix="orchestrator-action-plan",
                prompt=plan_prompt,
            )
            steps = result_text.strip().split("\n")
            # Clean up the steps
            steps = [
                step.strip().lstrip("0123456789. ")
                for step in steps
                if step.strip()
            ]
            if not steps:
                return {"steps": ["Please try creating your action plan again"]}
            return {"steps": steps[:7]}  # Limit to 7 steps
        except Exception as e:
            print(f"❌ Error creating action plan: {str(e)}")
            return {"steps": ["Please try creating your action plan again"]}
