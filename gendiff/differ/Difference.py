class Difference:
    def __init__(self, key: str, status: str, value=None, old_value=None,
                 children=None):
        self.key = key
        self.status = status
        self.value = value
        self.old_value = old_value
        self.children = children
