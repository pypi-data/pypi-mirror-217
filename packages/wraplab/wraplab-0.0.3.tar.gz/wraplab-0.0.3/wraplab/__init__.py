from engine import add

def inside_init(a: int) -> int:
    return a * 10

__version__ = "0.0.3"

__all__ = [
    "add",
    "inside_init"
]