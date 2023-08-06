from engine import some_fn_python_name

def inside_init(a: int) -> int:
    return a * 10

__version__ = "0.0.2"

__all__ = [
    "some_fn_python_name",
    "inside_init"
]