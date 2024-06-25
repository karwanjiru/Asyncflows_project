from asyncflows import AsyncFlows


async def main():
    query = input("Enter contents of Medical document to get an analysis:")
    flow = AsyncFlows.from_file("project.yaml").set_vars(
        query=query,
    )

    # Run the flow and return the default output (result of the analysis)
    result = await flow.run()
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())