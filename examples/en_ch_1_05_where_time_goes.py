import time
from contextlib import contextmanager

@contextmanager
def account(label: str):
    wall = time.perf_counter()
    cpu = time.process_time()          # CPU time only
    try:
        yield
    finally:
        elapsed = time.perf_counter() - wall
        burned = time.process_time() - cpu
        share = burned / elapsed if elapsed else 0.0
        print(f"{label}: total {elapsed:.3f} s, on CPU {burned:.3f} s "
              f"({share:.0%}); waiting {elapsed - burned:.3f} s")
