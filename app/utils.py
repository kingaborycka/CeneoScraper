

#funkcja do ekstrakcji składowych opinii
def extract_feature(opinion,selector, attribute = None ):
    try:
        if not attribute:
            return opinion.select(selector).pop(0).get_text().strip()
        else:
            return opinion.select(selector).pop(0)[attribute]
    except IndexError:
        return None

#funkcja do usuwania znaków formatujących
def remove_whitespaces(text):
    try:
        for char in ['\n','\r']:
            return text.replace(char,'.')
    except AttributeError:
        pass