# agentic_ai.py
import asyncio
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# 1. Define a tool properly
def echo_tool(text: str) -> str:
    """Echoes the user input back."""
    return f"Echo: {text}"

# Wrap the function into a FunctionTool
echo = FunctionTool.from_function(echo_tool)

# 2. Construct the agent
agent = Agent(
    name="EchoAgent",
    description="Echos whatever the user says.",
    tools=[echo]
)

async def main():
    print("Agent running. Type 'exit' to quit.")

    session_service = InMemorySessionService()
    runner = Runner(session_service=session_service, agent=agent)

    async with session_service.create_session(user_id="user1") as sess:
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            # Process interaction via events
            async for event in runner.run_async(sess, user_input):
                if event.content:
                    print(f"Agent: {event.content}")

if __name__ == "__main__":
    asyncio.run(main())
