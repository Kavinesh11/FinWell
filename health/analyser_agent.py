from uagents import Agent, Context
from uagents.protocols.chat import ChatProtocol, ChatMessage

analyser_agent = Agent(name="analyser_agent", seed="analyser_agent_seed")
chat = ChatProtocol()

@chat.on_message
async def default_handler(ctx: Context, msg: ChatMessage):
    result = f"📈 Here's a response for: {msg.content}"
    await ctx.send(msg.sender, ChatMessage(content=result))

analyser_agent.include(chat)

from uagents import Agent, Context, Model

class Message(Model):
    query: str
    response: str = None

class MedicationResponse(Model):
    response: str

class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

class SymptomResponse(Model):
    response: str

# FIXED AGENT ADDRESSES
ASI_AGENT_ID = "agent1qt69zmtdwud67k7t3nmp353l0y7u8j3q6t9fdy6f4v54258huxre6pnxgwz"
CLI_AGENT_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"  # Fixed
INSURANCE_AGENT_ADDRESS = "agent1qvwjtya8ncl5shwr7m8p80jw7l20lplt0ahtx40gzl3vsaeq4jr3kzuhfz4"

agent = Agent(
    name="AnalyserAgent",
    seed="analyser_seed",
    port=8006,
    endpoint=["http://localhost:8006/submit"],
    mailbox=True
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("📊 Analyzer Agent is live!")

async def prompting(query: str):
    return (
        f"Respond to the following user request about medication: {query}. "
        f"Provide reminders, dosage info, or any safety suggestions as needed."
    )

@agent.on_message(model=Message)
async def forward_to_asi(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"📨 Received user query: {msg.query}")
    prompt = await prompting(msg.query)
    await ctx.send(ASI_AGENT_ID, ASI1miniRequest(query=prompt))

@agent.on_message(model=ASI1miniResponse)
async def analyze_and_respond(ctx: Context, sender: str, msg: ASI1miniResponse):
    ctx.logger.info(f"📊 Analyzing ASI1 response: {msg.response}")
    
    # Example processing
    summary = f"[Analyzed] {msg.response}"  # Replace with real NLP, rules, or logic

    try:
        # Send analyzed result back to CLI
        await ctx.send(CLI_AGENT_ADDRESS, SymptomResponse(response=summary))
        ctx.logger.info("✅ Sent response to CLI agent")
        
        # Also send to insurance agent for evaluation
        await ctx.send(INSURANCE_AGENT_ADDRESS, SymptomResponse(response=summary))
        ctx.logger.info("✅ Sent response to insurance agent")
        
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send responses: {e}")

if __name__ == "__main__":
    agent.run()