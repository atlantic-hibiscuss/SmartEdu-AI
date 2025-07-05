# async_example.py
# Asynchronous Programming practice for Week 1

import asyncio

async def greet_user(name):
    await asyncio.sleep(1)  # Simulate async I/O task (shortened for testing speed)
    return f"Hello, {name}!"

async def main():
    # Run both greetings together so we do not wait on them one by one.
    result = await asyncio.gather(
        greet_user("Riyash"),
        greet_user("Mimo")
    )
    print(result)  # Output: ['Hello, Riyash!', 'Hello, Mimo!']

if __name__ == "__main__":
    asyncio.run(main())
