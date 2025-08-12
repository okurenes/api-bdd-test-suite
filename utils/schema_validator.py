import jsonschema

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id":    {"type": "integer"},
        "name":  {"type": "string"},
        "email": {"type": "string"},
    },
}

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "userId": {"type": "integer"},
    },
}

TODO_SCHEMA = {
    "type": "object",
    "required": ["id", "userId", "title", "completed"],
    "properties": {
        "id":        {"type": "integer"},
        "userId":    {"type": "integer"},
        "title":     {"type": "string"},
        "completed": {"type": "boolean"},
    },
}


def validate(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")
