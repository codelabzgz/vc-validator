# Propiedad de S.M. Codelab

# Cosas a validar
#   - Número de movimientos en primera línea == suma movimientos en cada línea  
#   - El ID de los puntos con S especificada está en la fila correspondiente 
#   - En cada ruta, los movimientos son correctos (no se atraviesan paredes ni avanza diagonalmente ni se saltan pasos sin agujero de gusano)
#   - Se pasa por todos los puntos
#   - Al realizar los movimientos especificados en la línea desde el origen tienes que obtener las mismas coordenadas que el punto definido con
#     el id en la línea

# Cosas a evaluar
#   - Si se valida correctamente -> determinar puntuación en base a número de movimientos

class MapConfig:
  def __init__(self, config_file):
    with open(config_file, 'r') as file:
      file_reader = iter(file.readline, '')
      self.dim = tuple(next(file_reader).split(';')) # (X, Y)
      self.initial_pos = tuple(next(file_reader).split(';')) # (x, y) 
      self.delivery_points = self.read_points(file_reader)
      self.walls = self.read_walls_or_tunnels(file_reader) 
      self.tunnels = self.read_walls_or_tunnels(file_reader) 

  def read_points(self, reader):
    """
    Delivery point type: id, coords, s
    Parse: X;Y[;S]
    """
    total_points = int(next(reader)) 
    delivery_points = []
    for point in range(total_points):
      next_point = next(reader).split(';') 
      delivery_points.append({
        "id": point + 1,
        "coords": (int(next_point[0]), int(next_point[1])),
        "s": None if len(next_point) <= 2 else int(next_point[2])
      })
    return delivery_points

  def read_walls_or_tunnels(self, reader):
    """
    Wall/Tunnel type: initial coords, final coords
    Parse: Xinit;Yinit:Xend;Yend
    """
    total_walls = int(next(reader))
    walls = []
    for wall in range(total_walls):
      next_wall = next(reader).split(':')
      walls.append({
        "init": tuple(map(int, next_wall[0].split(';'))),
        "end": tuple(map(int, next_wall[1].split(';')))
      })
    return walls
  
  def find_point(self, point_id):
    filtered_point = filter(lambda point: point.id == point_id, self.delivery_points)
    return None if len(filtered_point) == 0 else filtered_point[0]

  def has_required_position(self, point_id):
    point = self.find_point(point_id)
    return point.s if point else None

  def tunnel_at(self, pos):
    return len(filter(lambda tun: tun == pos, self.tunnels)) > 0 

  def wall_at(self, pos):
    return len(filter(lambda wall: wall == pos, self.walls)) > 0 
  
  def traverse_path(self, origin, movs):
    # origin -> (column, row)
    curr_pos = origin
    for mov in movs:
      (col, row) = origin
      match mov:
        case '>':
          if col+1 == self.dim[0]:
            return None, f"Drone gets out of map at X={self.dim[0]}" 
          curr_pos = (col+1, row)
        case '<':
          if col == 0:
            return None, "Drone gets out of map at X=0" 
          curr_pos = (col-1, row)
        case '+':
          if row == 0:
            return None, "Drone gets out of map at Y=0" 
          curr_pos = (col, row-1)
        case '-':
          if row+1 == self.dim[1]:
            return None, f"Drone gets out of map at Y={self.dim[1]}"
          curr_pos = (col, row+1)
        case other:
          return None, f"Unexpected movement type found: {other}"

      if (tunnel := self.tunnel_at(curr_pos)) is not None:
        curr_pos = tunnel_exit
      elif not self.wall_at(curr_pos):
        return None, f"Drone crushed into a wall at {curr_pos}!!"

    return curr_pos, None


  def coords_of_id(self, point_id):
    point = self.find_point(point_id)
    return point.coords if point else None

  def contains_all_dpoints(self, ids):
    expected_ids = set(map(lambda p: p.point_id, self.delivery_points))
    received_ids = set(ids)
    return expected_ids - received_ids == {}



def parse_route(raw_route):
  [ point_id, initial_coords, movs ] = raw_route.split(';')
  return {
    "point_id": point_id,
    "initial_coords": tuple(initial_coords.split('-')),
    "movs": movs
  }



def validate_output(config, output_file):
  with open(output_file, 'r') as file:
    file_reader = iter(file.readline, '')
    reported_movs = int(next(file_reader))
    delivery_points = []

    curr_point = 1
    for route in file_reader:
      route = parse_route(route)
      if (pos := conf.has_required_position(route.point_id)) is not None and curr_point != pos:
        return None, f"Delivery point with id {route.point_id} needs to be at position {pos}, found at {curr_point}"
      
      coords, err = config.traverse_path(route.initial_coords, movs)
      if err == None:
        return None, err
      
      if coords != config.coords_of_id(route.point_id):
        return None, f"Movements to reach delivery point with id {route.point_id} from {route.initial_coords} end up at {coords}"

      reported_movs -= len(movs)
      delivery_points.append(route.point_id)
      
      curr_point +=+ 1

  if reported_movs != 0:
    return None, f"Reported movements at beginning of file don't match those in the routes, differ by {abs(reported_movs)}"
  if not config.contains_all_dpoints(delivery_points):
    return None, "Drone doesn't visit all of the delivery points" 
