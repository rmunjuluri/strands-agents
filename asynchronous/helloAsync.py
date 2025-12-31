import asyncio

async def main():
    print("Hello...")
    # The 'await' keyword yields control to the event loop, allowing other tasks to run.
    await asyncio.sleep(5) 
    print("World!")

# The asyncio.run() function is used to execute the top-level async function
asyncio.run(main())
