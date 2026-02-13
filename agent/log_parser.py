def parse_error_blocks(error_log: str):
    """
    Splits log into individual traceback blocks.
    Returns list of (error_block, file_path) tuples.
    """
    blocks = error_log.split("Traceback")
    parsed = []

    for block in blocks:
        if not block.strip():
            continue

        block = "Traceback" + block

        file_path = None
        for line in block.splitlines():
            if 'File "' in line:
                file_path = line.split('File "')[1].split('"')[0]
                break

        if file_path:
            parsed.append((block, file_path))

    return parsed