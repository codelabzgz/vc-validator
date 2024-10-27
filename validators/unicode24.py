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

import re


class MapConfig:
  def __init__(self, config_file, level):
    self.level = level
    with open(config_file, 'r') as file:
      file_reader = iter(file.readline, '')
      self.dim = tuple(map(int, next(file_reader).split(';'))) # (X, Y)
      self.initial_pos = tuple(next(file_reader).split(',')) # (x, y) 
      self.delivery_points = self.read_points(file_reader)
      if level > 1:
        walls_ = self.read_walls_or_tunnels(file_reader) 
        # Transform wall ranges into all the positions that contain a wall
        # Otherwise, for every point you would have to check whether the drone
        # crashes into a wall, because you can't tell from origin and end positions
        # of the drone
        self.walls = []
        for wall in walls_:
          # Walls are not diagonal
          if wall["init"][0] == wall["end"][0]: # Vertical wall
            self.walls += [(wall["init"][0], y) for y in range(wall["init"][1], wall["end"][1]+1)]
          else: # Horizontal wall
            self.walls += [(x, wall["init"][1]) for x in range(wall["init"][0], wall["end"][0]+1)]

        self.tunnels = self.read_walls_or_tunnels(file_reader) 
        
      if level > 2:
        self.drones = self.read_drones(file_reader) 

  def read_points(self, reader):
    """
    Delivery point type: id, coords, s
    Parse: X;Y[;S]
    """
    total_points = int(next(reader)) 
    delivery_points = []
    for point in range(total_points):
      next_point = next(reader).split(',') 
      delivery_points.append({
        "point_id": point + 1,
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
      next_wall = next(reader).split(';')
      walls.append({
        "init": tuple(map(int, next_wall[0].split(','))),
        "end": tuple(map(int, next_wall[1].split(',')))
      })
    return walls
  
  def read_drones(self, reader):
    """
    Drone type: { position: (X,Y); movs: unfolded_movs; next_mov: index of next mov in movs  }
    Parse: X,Y;movs 
    """
    total_drones = int(next(reader))
    drones = []
    for _ in range(total_drones):
      next_drone = next(reader).split(';')
      matched_movs = re.findall(r'\d+[><+-]', next_drone[1])
      unfolded_movs = ""
      for mov in matched_movs:
        num_movs_of_type, mov_type = int(mov[:-1]), mov[-1]
        unfolded_movs += mov_type * num_movs_of_type
      drones.append({
        "position": tuple(map(int, next_drone[0].split(','))), 
        "movs": unfolded_movs, 
        "next_mov": 0 
      })
    return drones
  
  def find_point(self, point_id):
    filtered_point = list(filter(lambda point: point["point_id"] == point_id, self.delivery_points))
    return None if len(filtered_point) == 0 else filtered_point[0]

  def has_required_position(self, point_id):
    point = self.find_point(point_id)
    print(f"Specific position is required for point id {point_id}: {point}")
    return point["s"]if point else None

  def tunnel_at(self, pos):
    filtered_tun = list(filter(lambda tun: tun["init"] == pos or tun["end"] == pos, self.tunnels))
    if len(filtered_tun) == 0:
      return None

    tun = filtered_tun[0]
    if tun["init"] == pos:
      return tun["end"]
    else:
      return tun["init"]

  def wall_at(self, pos):
    return len(list(filter(lambda wall: wall == pos, self.walls))) > 0 

  def check_drone_collision(self, drone, pos, prev_pos):
    drone_prev_pos = drone["position"]
    drone_next_pos, err = self.move_drone(drone_prev_pos, drone["movs"][drone["next_mov"]]) 
    if err is not None:
      drone_next_pos = (drone_next_pos[0] % self.dim[1], drone_next_pos[1] % self.dim[0])
    if drone_prev_pos[0] == drone_next_pos[0] and pos[0] == prev_pos[0]: # Movimiento eje vertical de ambos
      return drone_next_pos == pos or drone_prev_pos == pos
    elif drone_prev_pos[1] == drone_next_pos[1] and pos[1] == prev_pos[1]: # Movimiento eje horizontal de ambos
      return drone_next_pos == pos or drone_prev_pos == pos
    else:
      return drone_next_pos == pos


  def drone_at(self, pos, prev_pos):
    return len(list(filter(lambda drone: self.check_drone_collision(drone, pos, prev_pos), self.drones))) > 0
  
  def update_drones_positions(self):
    
    for drone in self.drones:
      drone_next_move = drone["movs"][drone["next_mov"]]
      drone_next_pos, err = self.move_drone(drone["position"], drone_next_move)
      if err is not None:
        drone_next_pos = (drone_next_pos[0] % self.dim[1], drone_next_pos[1] % self.dim[0])
      drone["position"] = drone_next_pos 
      drone["next_mov"] = (drone["next_mov"] + 1) % len(drone["movs"])
  

  def move_drone(self, pos, mov_type):
    col, row = pos 
    final_pos, err = None, None
    match mov_type:
      case '>':
        if col+1 >= self.dim[0]:
          err = f"Drone gets out of map at X={self.dim[0]}" 
        final_pos = (col+1, row)
      case '<':
        if col-1 < 0:
          err = "Drone gets out of map at X<0" 
        final_pos = (col-1, row)
      case '+':
        if row-1 < 0:
          err = "Drone gets out of map at Y<0" 
        final_pos = (col, row-1)
      case '-':
        if row+1 >= self.dim[1]:
          err = f"Drone gets out of map at Y={self.dim[1]}"
        final_pos = (col, row+1)
      case other:
        err = f"Unexpected movement type found: {other}"
    return final_pos, err
    

  
  def traverse_path(self, origin, movs):
    # origin -> (column, row)
    curr_pos = origin
    matched_movs = re.findall(r'\d+[><+-]', movs)
    print(f"Path traversal from origin: {origin}")
    total_path_movements = 0
    prev_pos = curr_pos
    for mov in matched_movs:
      num_movs_of_type, mov_type = int(mov[:-1]), mov[-1]
      for num_mov in range(num_movs_of_type): 
        print(curr_pos)
        curr_pos, err = self.move_drone(curr_pos, mov_type)
        if err is not None:
          return None, None, err

        if self.level > 1:
          if (tunnel_exit := self.tunnel_at(curr_pos)) is not None:
            curr_pos = tunnel_exit
          if self.wall_at(curr_pos):
            return None, None, f"Drone crushed into a wall at {curr_pos}!!"
        if self.level > 2:
          if self.drone_at(curr_pos, prev_pos):
            return None, None, f"Your drone collided with another drone at {curr_pos} (Nobody was hurt ;)"
          self.update_drones_positions()
        prev_pos = curr_pos
        
      total_path_movements += num_movs_of_type

    return curr_pos, total_path_movements, None


  def coords_of_id(self, point_id):
    point = self.find_point(point_id)
    return point["coords"] if point else None

  def contains_all_dpoints(self, ids):
    expected_ids = set(map(lambda p: p["point_id"], self.delivery_points))
    received_ids = set(ids)
    # not bool({}) == True
    return not bool(expected_ids - received_ids)



def parse_route(raw_route):
  print(raw_route)
  [ point_id, initial_coords, movs ] = raw_route.split(';')
  return {
    "point_id": int(point_id),
    "initial_coords": tuple(map(int, initial_coords.split(','))),
    "movs": movs.strip()
  }



def validate_output(config, file_content):
  print(file_content)
  file_content = file_content.split('\n')
  print(file_content)
  reported_movs = int(file_content[0])
  total_movs = 0
  delivery_points = []

  curr_point = 1
  for route in file_content[1:]:
    if route.strip() == "":
      continue
    print(f"--- PROCESSING ROUTE AT LINE {curr_point} ---")
    
    route = parse_route(route)
    print(f"Route info: {route}")

    if (pos := config.has_required_position(route["point_id"])) is not None and curr_point != pos:
      return None, f"Delivery point with id {route["point_id"]} needs to be at position {pos}, found at {curr_point}"
    
    print("Route is well placed")
    
    coords, path_movs, err = config.traverse_path(route["initial_coords"], route["movs"])
    if err != None:
      return None, err
    
    print("Drone doesn't crash or get out of map")
    
    if coords != (expected_coords := config.coords_of_id(route["point_id"])):
      return None, f"Movements to reach delivery point with id {route["point_id"]} from {route["initial_coords"]} end up at {coords}, expected {expected_coords}"

    total_movs += path_movs 
    delivery_points.append(route["point_id"])
    
    curr_point +=+ 1

  if reported_movs != total_movs: 
    return None, f"Reported movements at beginning of file don't match those in the routes, differ by {abs(reported_movs-total_movs)}"
  if not config.contains_all_dpoints(delivery_points):
    return None, "Drone doesn't visit all of the delivery points" 
  
  return reported_movs, None

def score(solution):
  return 1000