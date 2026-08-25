# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import bias, scores, weights  # noqa: F401
# ─── листинг ───
import numpy as np

out = np.empty_like(scores)
np.multiply(scores, weights, out=out)     # результат пишется в готовый массив
np.add(out, bias, out=out)                # и обновляется на месте
