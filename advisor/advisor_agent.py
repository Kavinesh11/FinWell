from uagents import Agent, Context
from uagents.protocols.chat import ChatProtocol, ChatMessage

advisor = Agent(name="advisor_agent", seed="advisor_seed_phrase")
chat = ChatProtocol()

# Replace with real addresses (AgentVerse or MCP)
ANALYST_ADDRESS = "agent1q0ejvvp7x302ulx05389ncdfellmag6up4d2raa9v7dfrjarh4v52237sq7"
NEWS_ADDRESS = "agent1xyz..."
CRYPTO_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
SOLANA_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
HEALTH_ADDRESS = "agent1qv3dag4483k5dv4wkcncy65xpyrq4hgwk6nvuf0xzrhfz33cxaqj6xpg9c7"

@chat.on_message
async def route_message(ctx: Context, msg: ChatMessage):
    content = msg.content.lower()

    if "stock" in content or "share" in content or "market" in content:
        await ctx.send(ANALYST_ADDRESS, ChatMessage(content=msg.content))
        await ctx.send(NEWS_ADDRESS, ChatMessage(content=msg.content))

    elif "crypto" in content or "bitcoin" in content or "solana" in content:
        await ctx.send(CRYPTO_ADDRESS, ChatMessage(content=msg.content))
        await ctx.send(SOLANA_ADDRESS, ChatMessage(content=msg.content))

    elif "health" in content or "symptom" in content or "insurance" in content:
        await ctx.send(HEALTH_ADDRESS, ChatMessage(content=msg.content))

    else:
        await ctx.send(msg.sender, ChatMessage(content="❓ Sorry, I couldn't understand your query."))

advisor.include(chat)
