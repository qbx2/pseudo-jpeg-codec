import numpy
from PIL import Image


class JPEGDecoder:
    def __init__(self, f):
        self.f = f

    def decode(self):
        self.f.seek(0)
        raise NotImplementedError

        img = Image.new()

        return img

    def save(self, filename):
        img = self.decode()
        import pdb; pdb.set_trace()
        img.save(filename)

