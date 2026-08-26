QUERY = """
MATCH (a:Entity {id: $start})-[r:RELATES*1..3]-(b:Entity)
WHERE b.kind IN $kinds
RETURN b.id AS id, b.name AS name, length(r) AS distance
ORDER BY distance
LIMIT $limit
"""

async def neighbours(session, start: str, kinds: list[str], limit: int = 50):
    result = await session.run(QUERY, start=start, kinds=kinds, limit=limit)
    return [record.data() async for record in result]
