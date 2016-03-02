from django.db.models.fields.files import ImageField,ImageFieldFile
from PIL import Image
import os #for handling the thumbnail files
def add_thumbs(img_file):
    """
    Modifies a string (filename, URL) containing an image filename, to insert
    '.thumb' before the file extension (which is changed to be '.jpg').
    """
    parts=img_file.split(".")
    parts.insert(-1,'thumb')#foo.png=>'.thumb.png'
    if parts[-1].lower() not in ['jpeg','jpg','png']: #if the extension of the file is not JPEG
        parts[-1]='jpg' #rename o jpg
    return ".".join(parts) #join the img_file parts with a dot becomes 'foo.thumb.jpg'

class ThumbnailImageFieldFile(ImageFieldFile):
    """
    Because the .path and .url getters are already defined, and they take care of the
    minute boilerplate required for safe operation (the call to self._require_file , seen in
    the previous snippet concerning _get_path ), we are free to omit that extra code.
    """
    def _get_thumb_path(self):
        return add_thumbs(self.path)
    thumb_path=property(_get_thumb_path)
    def _get_thumb_url(self):
        return add_thumbs(self.url)
    thumb_url=property(_get_thumb_url)
    def save(self,name,content,save=True):
        super(ThumbnailImageFieldFile, self).save(name,content,save)
        img=Image.open(self.path)#opening the original image
        img.thumbnail((self.field.thumb_width,self.field.thumb_height),Image.ANTIALIAS)# creating the thumbnail
        img.save(self.thumb_path)
    def delete(self,save=True):
        """make sure our thumbnails are deleted after w delete the parent image"""
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)#if thumbnil exists fot this image
        super(ThumbnailImageFieldFile, self).delete(save)
class ThumbnailImageField(ImageField):
    """
`   Behaves like a regular ImageField, but stores an extra (JPEG) thumbnail
    image, providing get_FIELD_thumb_url() and get_FIELD_thumb_filename().
    Accepts two additional, optional arguments: thumb_width and thumb_height,
    both defaulting to 128 (pixels). Resizing will preserve aspect ratio while
    staying inside the requested dimensions; see PIL’s Image.thumbnail()
    method documentation for details.
    """ 
    attr_class=ThumbnailImageFieldFile
    
    def __init__(self,thumb_width=128,thumb_height=128,*args,**kwargs):
        self.thumb_width=thumb_width
        self.thumb_height=thumb_height
        super(ThumbnailImageField, self).__init__(*args,**kwargs)

    
