from django.utils.text import slugify

from a_social_project.utils import get_random_str, get_file_ext


def profile_image_upload_path(instance, file):
    username = f"{slugify(instance.user.username)}_{get_random_str(size=5)}"
    filename, ext = get_file_ext(file)
    new_filename = f"{username}{ext}"
    final_path = f"Profiles/{slugify(instance.user.username)}/{new_filename}"
    return final_path
