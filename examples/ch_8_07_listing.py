# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import HYDE_PROMPT, hashlib  # noqa: F401
# ─── листинг ───
PROMPT_VERSION = hashlib.blake2b(HYDE_PROMPT.encode("utf-8"),
                                 digest_size=6).hexdigest()
