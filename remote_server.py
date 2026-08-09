import random
from fastmcp import FastMCP

#create the fastMCP instence
mcp = FastMCP(name='Simple Calculator Server')


@mcp.tool
def roll_dice(n_dice:int =1 )->list[int]:
    """Rool n_dice 6 sided dice qnd return the result"""
    return [random.randint(1,6) for _ in range(n_dice)]


@mcp.tool
def add_number(a:float,b:float)->float:
    """Return the sum of a and b"""
    return a+b


#this is how we run the mcp server
if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
