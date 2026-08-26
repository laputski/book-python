# Извлечено из пособия автоматически. Строки до отметки в листинг не входят.
from stubs import Message, Model, OutputContractError, explain  # noqa: F401
# ─── листинг ───
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
                "The reply does not conform to the schema. Correct the issues listed "
                f"below and return only the corrected document.\n{explain(error)}"))
    raise AssertionError("unreachable")
