from enum import Enum, auto

class TokenType(Enum):
    # 1. Palabras reservadas
    KEYWORD = auto()
    
    # 2. nombres de variables
    IDENTIFIER = auto()
    
    # 3. Literales 
    NUMBER = auto()    # Para 50, 3.5
    STRING = auto()    # Para "Gandalf"
    
    # 4. Operadores 
    OPERATOR = auto()
    
    # 5. Puntuación ({, }, ;, ,, .)
    DELIMITER = auto()

    UNKNOWN = auto()   # Símbolo raro
    EOF = auto()