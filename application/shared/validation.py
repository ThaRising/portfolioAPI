def validate_base64(bytes_):
    if (len(bytes_) * (3 / 4)) - 1 <= 10000000:
        return True
    return False


def validate_uploads(files):
    if len(files) > 20:
        return False
    for file in files:
        validate_base64(file.get("uri"))
