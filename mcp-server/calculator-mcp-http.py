from fastmcp import FastMCP

mcp = FastMCP("Calculator HTTP Server")

@mcp.tool(description="Add two numbers together")
def add(x: int, y: int) -> int:
    """Add two numbers and return the result."""
    return x + y

@mcp.tool(description="Subtracts two numbers")
def subtract(x: int, y: int) -> int:
    """Subtract two numbers and return the result."""
    return x - y

@mcp.tool(description="Multiply two numbers together")
def multiply(x: int, y: int) -> int:
    """Multiply two numbers and return the result."""
    return x * y

@mcp.tool(description="Divide two numbers ")
def divide(x: int, y: int) -> float:
    """Divide two numbers and return the result."""
    return x / y

if __name__ == "__main__":
    mcp.run(transport="streamable-http")