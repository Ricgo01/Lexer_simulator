from token_type import TokenType
from token import Token

class Lexer:
    def __init__(self, source_code, symbol_table):
        self.source = source_code
        self.symbol_table = symbol_table
        
        # Punteros
        self.pos = 0
        self.line = 1
        self.col = 1
        
        self.tokens = []
        
        # Palabras reservadas de Java
        self.keywords = {
            "public", "class", "static", "void", "final", "int", "double", 
            "String", "new", "if", "else", "return", "true", "false", "private"
        }
    
    def current_char(self):
        if self.pos >= len(self.source):
            return None 
        return self.source[self.pos]

    def peek(self):
        """Mira el siguiente caracter sin avanzar"""
        if self.pos + 1 >= len(self.source):
            return None
        return self.source[self.pos + 1]

    def advance(self):
        """Avanza el puntero un paso"""
        if self.current_char() == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1

    def add_token(self, type_token, value):
        new_token = Token(type_token, value, self.line, self.col)
        self.tokens.append(new_token)


    def scan_identifier(self):
        """Lee palabras completas(Variables o Keywords)"""
        start_col = self.col
        buffer = ""
        
        # Mientras sea letra, dígito o guion bajo, seguimos leyendo
        while self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == '_'):
            buffer += self.current_char()
            self.advance()

        # Al terminar, decidimos qué es
        if buffer in self.keywords:
            # Es palabra reservada (public, class...)
            self.tokens.append(Token(TokenType.KEYWORD, buffer, self.line, start_col))
        else:
            # Es un identificador (variable)
            self.tokens.append(Token(TokenType.IDENTIFIER, buffer, self.line, start_col))

            self.symbol_table.put(buffer, "IDENTIFIER", self.line)

    def scan_number(self):
        """Lee números enteros o decimales"""
        start_col = self.col
        buffer = ""
        
        while self.current_char() is not None and (self.current_char().isdigit() or self.current_char() == '.'):
            buffer += self.current_char()
            self.advance()
            
        self.tokens.append(Token(TokenType.NUMBER, buffer, self.line, start_col))

    def scan_string(self):
        """Lee texto entre comillas"""
        start_col = self.col
        buffer = ""
        self.advance() # Saltamos la comilla de apertura "
        
        while self.current_char() is not None and self.current_char() != '"':
            buffer += self.current_char()
            self.advance()
            
        self.advance() 
        self.tokens.append(Token(TokenType.STRING, buffer, self.line, start_col))

    def skip_comment(self):
        """Se salta todo hasta el final de la línea"""
        while self.current_char() is not None and self.current_char() != '\n':
            self.advance()

    def skip_block_comment(self):
        """Se salta todo hasta encontrar */"""
        self.advance() 
        self.advance() 
        while self.current_char() is not None:
            if self.current_char() == '*' and self.peek() == '/':
                self.advance() 
                self.advance() 
                break
            self.advance()


    def tokenize(self):
        while self.pos < len(self.source):
            char = self.current_char()

            # Espacios en blanco
            if char.isspace():
                self.advance()
                continue
            
            # Comentarios o División (Lookahead)
            if char == '/':
                if self.peek() == '/': 
                    self.skip_comment()
                    continue
                elif self.peek() == '*': 
                    self.skip_block_comment()
                    continue
                else: # Es división normal
                    self.add_token(TokenType.OPERATOR, "/")
                    self.advance()
                    continue

            #Identificadores y Palabras clave
            if char.isalpha() or char == '_':
                self.scan_identifier()
                continue

            #Números
            if char.isdigit():
                self.scan_number()
                continue

            #Strings
            if char == '"':
                self.scan_string()
                continue

            #Operadores y Delimitadores
            if char in {'{', '}', '(', ')', '[', ']', ';', ',', '.'}:
                self.add_token(TokenType.DELIMITER, char)
                self.advance()
                continue
            
            if char in {'+', '-', '*', '=', '<', '>', '!'}:
                next_char = self.peek()
                
                #  ==, +=, -=, *=, <=, >=, !=
                if next_char == '=':
                    self.add_token(TokenType.OPERATOR, char + "=")
                    self.advance() # Consumir actual
                    self.advance() # Consumir el '='
                    continue

                #  ++, --
                if char == '+' and next_char == '+':
                    self.add_token(TokenType.OPERATOR, "++")
                    self.advance()
                    self.advance()
                    continue
                    
                if char == '-' and next_char == '-':
                    self.add_token(TokenType.OPERATOR, "--")
                    self.advance()
                    self.advance()
                    continue

                self.add_token(TokenType.OPERATOR, char)
                self.advance()
                continue
            
            print(f"Caracter extraño encontrado: {char}")
            self.advance()
        
        return self.tokens