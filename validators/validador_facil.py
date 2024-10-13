import re


def read_input_file(file_path):
    """
    Función para leer el archivo de entrada y extraer los datos necesarios
    :param 
            file_path: Ruta del archivo de entrada
    :return: 
            map_size: Tupla que contiene el tamaño del mapa
            initial_position: La posición inicial del dron
            points: Una tupla de la lista de puntos con coordenadas y el orden especial
    """

    # Abre el archivo en modo lectura
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Leer el tamaño del mapa
    map_size = tuple(map(int, lines[0].strip().split(';')))
    # Leer la posición inicial del dron
    initial_position = tuple(map(int, lines[1].strip().split(';')))
    # Leer el número total de puntos
    num_points = int(lines[2].strip())
    
    points = []
    # Leer las coordenadas de cada punto y el orden especial si existe
    for line in lines[3:3+num_points]:
        # Eliminar espacios en blanco y dividir la línea en partes
        parts = list(map(int, line.strip().split(';')))
    
        # Si la línea tiene solo dos partes, es un punto sin orden especial
        if len(parts) == 2:
            points.append((parts[0], parts[1], None))       # Punto sin orden especial
        else:
            points.append((parts[0], parts[1], parts[2]))   # Punto con orden especial

    # Convertir la lista de puntos en una tupla para hacerla inmutable
    points = tuple(points)
    # Devuelve el tamaño del mapa, la posición inicial y la lista de puntos
    return map_size, initial_position, points


def read_output_file(file_path):
    """
    Función para leer el archivo de salida proporcionado por el participante y extraer los datos necesarios
    :param 
            file_path: Ruta del archivo de entrada
    :return: 
            total_movements: Número total de movimientos realizados por el dron
            routes: Una tupla de la lista de rutas con ID de punto, coordenadas iniciales y direcciones de movimiento
    """

    # Abre el archivo en modo lectura
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Lee el número total de movimientos desde la primera línea
    total_movements = int(lines[0].strip())
    
    # Inicializa una lista para almacenar las rutas
    routes = []
    
    # Itera sobre las líneas restantes del archivo
    for line in lines[1:]:
        # Usa una expresión regular para extraer los datos de cada línea
        match = re.match(r'(\d+);(\d+)-(\d+);([><+-]+)', line.strip())
        
        # Si la línea coincide con el formato esperado
        if match:
            # Extrae y convierte los datos a los tipos apropiados
            point_id = int(match.group(1))  # ID del punto
            start_x = int(match.group(2))   # Coordenada X inicial
            start_y = int(match.group(3))   # Coordenada Y inicial
            directions = match.group(4)     # Direcciones de movimiento
            
            # Añade los datos extraídos a la lista de rutas
            routes.append((point_id, start_x, start_y, directions))
        else:
            # Lanza una excepción si la línea no coincide con el formato esperado
            raise ValueError(f"Invalid route format: {line.strip()}")
    
    # Convertir la lista de rutas en una tupla para hacerla inmutable
    routes = tuple(routes)
    # Devuelve el número total de movimientos y la lista de rutas
    return total_movements, routes


def validate_output_data(map_size, initial_position, points, total_movements, routes):
    """
    Función para validar los datos de salida proporcionados por el participante
    :param 
            map_size: Tupla que contiene el tamaño del mapa
            initial_position: La posición inicial del dron
            points: Una tupla de la lista de puntos con coordenadas y el orden especial
            total_movements: Número total de movimientos realizados por el dron
            routes: Una tupla de la lista de rutas con ID de punto, coordenadas iniciales y direcciones de movimiento
    """

    # Inicializar un conjunto para llevar un registro de los puntos visitados
    visited_points = set()
    # Establecer la posición actual a la posición inicial
    current_position = initial_position
    # Inicializar el contador de movimientos a cero
    movement_count = 0
    # Inicializar el contador de puntos visitados a uno
    visited_points_count = 1
    
    # Iterar sobre cada ruta
    for point_id, start_x, start_y, directions in routes:
        # Verificar si la posición de inicio de la ruta coincide con la posición actual
        if (start_x, start_y) != current_position:
            raise ValueError(f"La posición de inicio de la ruta {start_x},{start_y} no coincide con la posición actual {current_position}")
        
        # Iterar sobre cada dirección en la ruta
        for direction in directions:
            # Actualizar la posición actual según la dirección
            if direction == '>':
                current_position = (current_position[0] + 1, current_position[1])
            elif direction == '<':
                current_position = (current_position[0] - 1, current_position[1])
            elif direction == '+':
                current_position = (current_position[0], current_position[1] + 1)
            elif direction == '-':
                current_position = (current_position[0], current_position[1] - 1)
            else:
                raise ValueError(f"Dirección inválida: {direction}")
            # Incrementar el contador de movimientos
            movement_count += 1

            # Verificar si la posición actual está dentro de los límites del mapa
            if current_position[0] < 0 or current_position[0] >= map_size[0] or current_position[1] < 0 or current_position[1] >= map_size[1]:
                raise ValueError(f"El dron se salió del mapa en la posición {current_position}")
        
        # Verificar si la posición actual coincide con la posición del punto visitado
        if current_position != points[point_id - 1][:2]:
            raise ValueError(f"El dron no llegó al punto {point_id} en la posición correcta")

        # Verificar si el punto visitado es un punto de orden especial
        if points[point_id - 1][2] is not None and points[point_id - 1][2] != visited_points_count:
            raise ValueError(f"El punto visitado {point_id} no es el siguiente punto de orden especial")

        # Añadir el ID del punto al conjunto de puntos visitados
        visited_points.add(point_id)
        visited_points_count += 1           # Incrementar el contador de puntos visitados
    
    # Verificar si el total de movimientos coincide con el total esperado
    if movement_count != total_movements:
        raise ValueError(f"El total de movimientos {movement_count} no coincide con el esperado {total_movements}")
    
    # Verificar si todos los puntos de orden especial fueron visitados en el orden correcto
    for i, (x, y, s) in enumerate(points):
        if (i + 1) not in visited_points:
            raise ValueError(f"El punto {i + 1} no fue visitado.")


def main(input_file, output_file):
    """
    Función principal para validar los datos de salida proporcionados por el participante
    :param
            input_file: Ruta del archivo de entrada
            output_file: Ruta del archivo de salida
    """

    # Leer los datos del archivo de entrada
    map_size, initial_position, points = read_input_file(input_file)
    
    # Leer los datos del archivo de salida
    total_movements, routes = read_output_file(output_file)
    
    # Validar los datos de salida usando los datos de entrada
    validate_output_data(map_size, initial_position, points, total_movements, routes)
    
    # Imprimir un mensaje de éxito si la validación es correcta
    print("Validation successful")


# if __name__ == "__main__":
#     # Definir el nombre del archivo de entrada
#     input_file = "input.txt"
    
#     # Definir el nombre del archivo de salida
#     output_file = "output.txt"
    
#     # Llamar a la función principal con los archivos de entrada y salida
#     main(input_file, output_file)
