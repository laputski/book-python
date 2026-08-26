# Extracted from the book automatically. Lines above the mark are not part of the listing.
from stubs import Message, Model, OutputContractError, explain  # noqa: F401
# --- the listing ---
from pydantic import BaseModel, ValidationError

async def ask_structured[T: BaseModel](model: Model, prompt: str, schema: type[T],
                                       attempts: int = 3) -> T:
    conversation = [Message.user(prompt)]
    for attempt in range(attempts):
        raw = await model.complete(conversation, response_schema=schema.model_json_schema())
        try:
            return schema.model_validate_json(raw)
        except ValidationError as error:
            if attempt == attempts - 1:
                raise OutputContractError(schema.__name__, raw) from error
            conversation.append(Message.assistant(raw))
            conversation.append(Message.user(
                "Ответ не соответствует схеме. Исправьте перечисленное "
                f"и верните только исправленный документ.\n{explain(error)}"))
    raise AssertionError("недостижимо")
