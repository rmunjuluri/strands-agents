import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

async def example():
    transport = StreamableHttpTransport("http://127.0.0.1:8000/mcp")
    async with Client(transport=transport) as client:
        await client.ping()
        print("Ping successful!")

        # List avaialble tools to confirm *** are available
        tools = await client.list_tools()
        print("Available tools: ", tools)

if __name__ == "__main__":
    asyncio.run(example())