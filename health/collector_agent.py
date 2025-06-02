from uagents import Agent, Context
from uagents.protocols.chat import ChatProtocol, ChatMessage

collector_agent = Agent(name="collector_agent", seed="collector_agent_seed")
chat = ChatProtocol()

@chat.on_message
async def default_handler(ctx: Context, msg: ChatMessage):
    result = f"📈 Here's a response for: {msg.content}"
    await ctx.send(msg.sender, ChatMessage(content=result))

collector_agent.include(chat)

from uagents import Agent, Context, Model

class Message(Model):
    query: str
    response: str = None

class SymptomResponse(Model):
    response: str

class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

# FIXED AGENT ADDRESSES TO MATCH
ASI_AGENT_ID = "agent1qt69zmtdwud67k7t3nmp353l0y7u8j3q6t9fdy6f4v54258huxre6pnxgwz"
CLI_AGENT_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"  # Fixed
ANALYSER_AGENT_ADDRESS = "agent1qdkulla80gkjdumy6qp867x6u9wwqkrya0r4eks6zs520lqp6r3g200d83u"
INSURANCE_AGENT_ADDRESS = "agent1qvwjtya8ncl5shwr7m8p80jw7l20lplt0ahtx40gzl3vsaeq4jr3kzuhfz4"

agent = Agent(
    name="CollectorAgent",
    seed="collector_seed",
    port=8005,
    endpoint=["http://127.0.0.1:8005/submit"],
    mailbox=True
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("🩺 Collector Agent is live!")

async def prompting(query: str):
    return (
        f"Based on the following symptoms: {query}, suggest possible causes and "
        f"recommend next steps or actions the user should take, such as home remedies, "
        f"consulting a doctor, or emergency care."
    )

@agent.on_message(model=Message)
async def forward_to_asi(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"📨 Received user symptoms: {msg.query}")
    prompt = await prompting(msg.query)
    await ctx.send(ASI_AGENT_ID, ASI1miniRequest(query=prompt))

@agent.on_message(model=ASI1miniResponse)
async def handle_asi_response(ctx: Context, sender: str, msg: ASI1miniResponse):
    ctx.logger.info(f"🤖 ASI1 responded: {msg.response}")
    # Send to analyzer for processing
    await ctx.send(ANALYSER_AGENT_ADDRESS, ASI1miniResponse(response=msg.response))

if __name__ == "__main__":
    agent.run()