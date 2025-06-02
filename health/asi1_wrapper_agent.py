from uagents import Agent, Context
from uagents.protocols.chat import ChatProtocol, ChatMessage

asi1_wrapper_agent = Agent(name="asi1_wrapper_agent", seed="asi1_wrapper_agent_seed")
chat = ChatProtocol()

@chat.on_message
async def default_handler(ctx: Context, msg: ChatMessage):
    result = f"📈 Here's a response for: {msg.content}"
    await ctx.send(msg.sender, ChatMessage(content=result))

asi1_wrapper_agent.include(chat)

from uagents import Agent, Context, Model
import requests

# Define schemas
class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

# Using the exact same seed to maintain the agent ID
asi1_agent = Agent(
    name="ASIWrapperAgent",
    seed="asi_wrapper_seed",
    port=8009,
    endpoint=["http://127.0.0.1:8009/submit"],
    mailbox=True
)

ASI1_LLM_ENDPOINT = "https://asi1.ai/chat"  # Placeholder for actual LLM endpoint
HEADERS = {
    "Authorization": "sk_d28825f98e2944d69f4f87750bcb711605e09bdda4a94176b467fc88fe11b19f",
    "Content-Type": "application/json"
}

@asi1_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("🧠 ASI1 Mini Wrapper Agent is live!")
    ctx.logger.info(f"Agent address: {asi1_agent.address}")

@asi1_agent.on_message(model=ASI1miniRequest)
async def handle_query(ctx: Context, sender: str, msg: ASI1miniRequest):
    ctx.logger.info(f"⚡ Received query from {sender}: {msg.query}")

    try:
        # 🧪 Mocked response — you can call a real endpoint here instead
        response = f"[Mock ASI Response] Insight based on your query: {msg.query}"
        ctx.logger.info(f"✅ Response generated: {response}")
        
        # Send response back to sender
        await ctx.send(sender, ASI1miniResponse(response=response))
        ctx.logger.info(f"✅ Response sent back to {sender}")
        
    except Exception as e:
        response = "Sorry, failed to reach ASI1 endpoint."
        ctx.logger.error(f"❌ Error: {str(e)}")
        await ctx.send(sender, ASI1miniResponse(response=response))

if __name__ == "__main__":
    asi1_agent.run()