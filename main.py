from lexer import Lexer
from symbol_table import SymbolTable

def cargar_codigo_desde_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return ""

if __name__ == "__main__":
    nombre_archivo = "codigo_fuente.java"
    
    codigo_java = cargar_codigo_desde_archivo(nombre_archivo)
    
    if codigo_java:
        print(f"--- Iniciando Scanner para: {nombre_archivo} ---\n")

        tabla_simbolos = SymbolTable()
        lexer = Lexer(codigo_java, tabla_simbolos)

        tokens = lexer.tokenize()

        print("LISTADO DE TOKENS:")
        print(f"{'LINEA':<8} | {'COL':<5} | {'TIPO':<15} | {'VALOR'}")
        print("-" * 50)
        for t in tokens:
            print(f"{t.line:<8} | {t.col:<5} | {t.type.name:<15} | {t.value}")
        
        tabla_simbolos.print_table()
    else:
        print("No se pudo cargar el código.")
