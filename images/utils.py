from django.utils.text import slugify

from a_social_project.utils import get_random_str, get_file_ext


def image_upload_path(instance, file):
    username = slugify(instance.user.username)
    filename, ext = get_file_ext(file)
    new_filename = f"{get_random_str()}{ext}"
    final_path = f"posts/{username}/{new_filename}"
    return final_path
