class SymbolTable:
    def __init__(self):
        self.table{}

    def put(self, name, type_info, line):
        if name not in self.symbols:
            # Estructura base
            data = {
                "tipo": type_info,
                "lineas": [line]  
            }
            
            #IDENTIFICADOR le asignamos un ID numérico
            if type_info == "IDENTIFIER":
                data["id"] = self.counter
                self.counter += 1
            else:
                data["id"] = None
            
            # Guardamos en el diccionario
            self.symbols[name] = data

        #El símbolo YA existe
        else:
            #Añadimos la nueva línea a la lista
            self.symbols[name]["lineas"].append(line)
    
    def print_table(self):
        print("\n=== TABLA DE SÍMBOLOS ===")
        print(f"{'ID':<5} | {'NOMBRE':<20} | {'TIPO':<15} | {'LINEAS'}")
        print("-" * 60)
        for name, data in self.symbols.items():
            lineas_str = ", ".join(map(str, data["lineas"]))
            id_str = str(data["id"]) if data["id"] else "-"
            
            print(f"{id_str:<5} | {name:<20} | {data['tipo']:<15} | {lineas_str}")

    