import uuid


def generate_code() -> str:
    verified_code = str(uuid.uuid4())
    return verified_code
