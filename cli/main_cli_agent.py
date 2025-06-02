from uagents import Agent, Context
from uagents.protocols.chat import ChatProtocol, ChatMessage

main_cli_agent = Agent(name="main_cli_agent", seed="main_cli_seed_phrase")
chat = ChatProtocol()

# Advisor address
ADVISOR_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"

@main_cli_agent.on_event("startup")
async def intro(ctx: Context):
    ctx.logger.info("🤖 Welcome to FinWell – Your Personal Finance & Wellness Copilot")

@main_cli_agent.on_interval(period=10)
async def query_input(ctx: Context):
    user_input = input("🧑 You: ").strip()
    if user_input:
        await ctx.send(ADVISOR_ADDRESS, ChatMessage(content=user_input))

@chat.on_message
async def show_reply(ctx: Context, msg: ChatMessage):
    print(f"🤖 FinWell: {msg.content}")

main_cli_agent.include(chat)
