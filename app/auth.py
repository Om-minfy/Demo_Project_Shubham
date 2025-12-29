import uuid

def create_access_token(user_id: int):
    return f"token-{user_id}-{uuid.uuid4()}"