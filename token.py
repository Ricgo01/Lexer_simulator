class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Line {self.line}:{self.col}  [{self.type.name}]  {self.value}"