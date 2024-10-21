import sys

sys.path.append("../../..")

from unicode24 import MapConfig, validate_output


def test_bad_route(config):
  # in test file, movements take origin to (40, 26)
  wrong_id = 3
  init_coords = (32, 32)
  expected_coords = (40, 25)
  bad_coords = (40, 26)
  _, err = validate_output(config, "bad_route.txt")
  assert err == f"Movements to reach delivery point with id {wrong_id} from {init_coords} end up at {bad_coords}, expected {expected_coords}", err
  print("Test test_bad_route: OK")

def test_id_not_in_place(config):
  wrong_id = 3
  expected_pos = 1
  found_pos = 2
  _, err = validate_output(config, "id_not_in_place.txt")
  assert err == f"Delivery point with id {wrong_id} needs to be at position {expected_pos}, found at {found_pos}", err
  print("Test test_id_not_in_place: OK")

def test_out_of_map_xlimit(config):
  x_limit = 100
  _, err = validate_output(config, "out_of_map_xlimit.txt")
  assert err == f"Drone gets out of map at X={x_limit}", err
  print("Test test_out_of_map_xlimit: OK") 

def test_out_of_map_ylimit(config):
  y_limit = 100
  _, err = validate_output(config, "out_of_map_ylimit.txt")
  assert err == f"Drone gets out of map at Y={y_limit}", err
  print("Test test_out_of_map_ylimit: OK") 

def test_out_of_map_x0(config):
  _, err = validate_output(config, "out_of_map_x0.txt")
  assert err == f"Drone gets out of map at X<0", err
  print("Test test_out_of_map_x0: OK") 

def test_out_of_map_y0(config):
  _, err = validate_output(config, "out_of_map_y0.txt")
  assert err == f"Drone gets out of map at Y<0", err
  print("Test test_out_of_map_y0: OK") 

def test_route_points_remaining(config):
  _, err = validate_output(config, "route_points_remaining.txt")
  assert err == "Drone doesn't visit all of the delivery points", err
  print("Test test_route_points_remaining: OK")


def test_wall(config):
  expected_crash = (23, 5)
  _, err = validate_output(config, "wall.txt")
  assert err == f"Drone crushed into a wall at {expected_crash}!!", err
  print("Test test_wall: OK")

def test_wrong_movs_reported(config):
  difference = 2
  _, err = validate_output(config, "wrong_movs_reported.txt")
  assert err == f"Reported movements at beginning of file don't match those in the routes, differ by {difference}", err
  print("Test test_wrong_movs_reported: OK")

def good(config):
  _, err = validate_output(config, "good.txt")
  assert err == None, err
  print("Test good: OK")

def test_drone_crash(config):
  expected_crash = (39, 0)
  _, err = validate_output(config, "drone_crash.txt")
  assert err == f"Your drone collided with another drone at {expected_crash} (Nobody was hurt ;)", err
  print("Test drone_crash: OK")

def main():
  config = MapConfig("input_medio.txt", 2) 
  test_bad_route(config)
  test_id_not_in_place(config)
  test_out_of_map_xlimit(config)
  test_out_of_map_ylimit(config)
  test_out_of_map_x0(config)
  test_out_of_map_y0(config)
  test_route_points_remaining(config)
  test_wall(config)
  test_wrong_movs_reported(config)
  good(config)
  config = MapConfig("input_dificil.txt", 3)
  test_drone_crash(config)


if __name__ == '__main__':
  main()


