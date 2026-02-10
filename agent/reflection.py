def should_retry(attempt, max_retries):
    return attempt < max_retries