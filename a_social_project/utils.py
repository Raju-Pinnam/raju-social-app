import os, string, random


def get_file_ext(file):
    basename = os.path.basename(file)
    filename, ext = os.path.splitext(basename)
    return filename, ext


def get_random_str(size=10, chars=string.ascii_uppercase + string.digits):
    rand_str = ''.join(random.choice(chars) for _ in range(size))
    return rand_str
