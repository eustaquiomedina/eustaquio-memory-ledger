def flatten_dict(d: dict, sep: str = ".") -> dict:
    """Return a flat dict whose nested keys are joined with sep."""
    flattened = {}

    def walk(prefix, value):
        if isinstance(value, dict):
            for key, child in value.items():
                next_key = str(key) if not prefix else f"{prefix}{sep}{key}"
                walk(next_key, child)
            return

        flattened[prefix] = value

    for key, value in d.items():
        walk(str(key), value)

    return flattened
