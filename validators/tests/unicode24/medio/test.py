import sys

sys.path.append("../../..")

from unicode24 import MapConfig, validate_output


def test_bad_route(config):
  # in test file, movements take origin to (40, 26)
  wrong_id = 3
  init_coords = (32, 32)
  expected_coords = (40, 25)
  bad_coords = (40, 26)
  with open("bad_route.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Movements to reach delivery point with id {wrong_id} from {init_coords} end up at {bad_coords}, expected {expected_coords}", err
  print("Test test_bad_route: OK")

def test_id_not_in_place(config):
  wrong_id = 3
  expected_pos = 1
  found_pos = 2
  with open("id_not_in_place.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Delivery point with id {wrong_id} needs to be at position {expected_pos}, found at {found_pos}", err
  print("Test test_id_not_in_place: OK")

def test_out_of_map_xlimit(config):
  x_limit = 100
  with open("out_of_map_xlimit.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Drone gets out of map at X={x_limit}", err
  print("Test test_out_of_map_xlimit: OK") 

def test_out_of_map_ylimit(config):
  y_limit = 100
  with open("out_of_map_ylimit.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Drone gets out of map at Y={y_limit}", err
  print("Test test_out_of_map_ylimit: OK") 

def test_out_of_map_x0(config):
  with open("out_of_map_x0.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Drone gets out of map at X<0", err
  print("Test test_out_of_map_x0: OK") 

def test_out_of_map_y0(config):
  with open("out_of_map_y0.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Drone gets out of map at Y<0", err
  print("Test test_out_of_map_y0: OK") 

def test_route_points_remaining(config):
  with open("route_points_remaining.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == "Drone doesn't visit all of the delivery points", err
  print("Test test_route_points_remaining: OK")


def test_wall(config):
  expected_crash = (23, 5)
  with open("wall.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Drone crushed into a wall at {expected_crash}!!", err
  print("Test test_wall: OK")

def test_wrong_movs_reported(config):
  difference = 2
  with open("wrong_movs_reported.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == f"Reported movements at beginning of file don't match those in the routes, differ by {difference}", err
  print("Test test_wrong_movs_reported: OK")

def good(config):
  with open("good.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
    assert err == None, err
  print("Test good: OK")

def test_drone_crash(config):
  expected_crash = (40, 0)
  with open("drone_crash.txt", "r") as file:
    _, err = validate_output(config, "".join(file.readlines()))
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


