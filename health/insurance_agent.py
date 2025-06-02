from uagents import Agent, Context
from uagents.protocols.chat import ChatProtocol, ChatMessage

insurance_agent = Agent(name="insurance_agent", seed="insurance_agent_seed")
chat = ChatProtocol()

@chat.on_message
async def default_handler(ctx: Context, msg: ChatMessage):
    result = f"📈 Here's a response for: {msg.content}"
    await ctx.send(msg.sender, ChatMessage(content=result))

insurance_agent.include(chat)

from uagents import Agent, Context, Model
import requests
from bs4 import BeautifulSoup

# Define message models
class SymptomResponse(Model):
    response: str

class InsuranceQuery(Model):
    income: int

class InsuranceOptions(Model):
    options: list

# Agent Addresses - FIXED TO MATCH MAIN.PY
INSURANCE_AGENT_ADDRESS = "agent1qvwjtya8ncl5shwr7m8p80jw7l20lplt0ahtx40gzl3vsaeq4jr3kzuhfz4"
CLI_AGENT_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"

# Initialize the Insurance Agent
insurance_agent = Agent(
    name="InsuranceAgent",
    seed="insurance_agent_seed",
    port=8010,
    endpoint=["http://127.0.0.1:8010/submit"],
    mailbox=True
)

@insurance_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("💼 Insurance Agent is live!")

@insurance_agent.on_message(model=SymptomResponse)
async def receive_analysis(ctx: Context, sender: str, msg: SymptomResponse):
    ctx.logger.info(f"🩺 Analyzed response: {msg.response}")

    # Check if the response contains serious condition keywords
    serious_keywords = [
        "chest pain", "emergency", "critical", "shortness of breath",
        "life-threatening", "serious", "this condition may be serious"
    ]
    if any(keyword in msg.response.lower() for keyword in serious_keywords):
        ctx.logger.info("⚠️ Serious condition detected. Asking about insurance.")
        prompt = "Do you have health insurance? If not, please enter your monthly income."
        await ctx.send(CLI_AGENT_ADDRESS, SymptomResponse(response=prompt))

@insurance_agent.on_message(model=InsuranceQuery)
async def suggest_insurance(ctx: Context, sender: str, msg: InsuranceQuery):
    income = msg.income
    ctx.logger.info(f"💰 Received income: ₹{income}")
    
    # Get insurance options
    options = get_top_insurance_plans(income)
    ctx.logger.info(f"📦 Sending {len(options)} insurance options to user.")
    
    try:
        # Send insurance options back to CLI
        await ctx.send(CLI_AGENT_ADDRESS, InsuranceOptions(options=options))
        ctx.logger.info("✅ Insurance options sent successfully")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send insurance options: {e}")

# Mock or scraping-based plan suggestion
def get_top_insurance_plans(income):
    """
    Mock insurance plan recommendations based on income brackets.
    Replace with real scraping or API calls if needed.
    """
    if income < 20000:
        return [
            "Star Health Medi-Classic",
            "Care Health Joy Plan",
            "HDFC ERGO Health Suraksha"
        ]
    elif income < 50000:
        return [
            "Niva Bupa ReAssure",
            "ICICI Lombard iHealth",
            "Tata AIG Medicare"
        ]
    else:
        return [
            "Max Bupa Health Companion",
            "HDFC ERGO Optima Restore",
            "Religare Care Supreme"
        ]

# Start the agent
if __name__ == "__main__":
    insurance_agent.run()