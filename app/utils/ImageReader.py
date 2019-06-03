from django.core.files.base import ContentFile
import six
import base64
import uuid
import imghdr

class ImageReader():
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data' in data and ';base64' in data:
                header, data = data.split(';base64')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                return

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = '%s.%s' % (file_name, file_extension)
            data = ContentFile(decoded_file, name=complete_file_name)
        return data

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = 'jpg' if extension=='jpeg' else extension
        return extension
