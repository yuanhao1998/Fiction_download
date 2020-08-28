class BookNameConverter:  # ÊéÃû
    regex = '.*'

    @staticmethod
    def to_python(value):
        return str(value)

    @staticmethod
    def to_url(value):
        return str(value)