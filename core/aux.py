from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size
    if filesize > 1000000:
        raise ValidationError("The maximum file size that can be uploaded is 1MB")
    else:
        return value


def generate_slug(my_model):
    my_objects = my_model.objects.all()
    x = my_objects.count()
    if x != 0:
        return int(my_objects[0].slug) + 1
    else:
        return 0
