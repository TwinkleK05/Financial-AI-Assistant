from api.schemas import AskRequest

request = AskRequest(
    question="What is Apple's market cap?",
    role="Finance"
)

print(request)