from engine.feedback import (
    save_feedback,
    get_feedback,
)

save_feedback(
    question="What is Apple's market cap?",
    chunk_id=None,
    rating=5,
    comment="Very helpful answer."
)

rows = get_feedback()

for row in rows:
    print(row)