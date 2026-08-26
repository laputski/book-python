import hashlib, json
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CacheKey:
    question: str
    model: str
    prompt_version: str
    temperature: float

    def digest(self) -> str:
        payload = json.dumps({
            "q": " ".join(self.question.lower().split()),   # question normalization
            "m": self.model,
            "p": self.prompt_version,
            "t": round(self.temperature, 2),
        }, ensure_ascii=False, sort_keys=True)
        return hashlib.blake2b(payload.encode("utf-8"), digest_size=16).hexdigest()
