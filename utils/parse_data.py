def parser(json, keys, default=None):
    try:
        value = json
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default
