def name(string: str) -> str:
    if len(string) >= 25:
        string = f'{string[:16]}...{string[-5:]}'

    return string


