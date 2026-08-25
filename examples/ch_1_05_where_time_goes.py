import time
from contextlib import contextmanager

@contextmanager
def account(label: str):
    wall = time.perf_counter()
    cpu = time.process_time()          # только время на процессоре
    try:
        yield
    finally:
        elapsed = time.perf_counter() - wall
        burned = time.process_time() - cpu
        share = burned / elapsed if elapsed else 0.0
        print(f"{label}: всего {elapsed:.3f} с, на процессоре {burned:.3f} с "
              f"({share:.0%}); ожидание {elapsed - burned:.3f} с")
