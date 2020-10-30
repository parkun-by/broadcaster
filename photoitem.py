class PhotoItem(dict):
    def __init__(self, media_type, media, caption, parse_mode='HTML'):
        dict.__init__(self,
                      type=media_type,
                      media=media,
                      caption=caption,
                      parse_mode=parse_mode)
