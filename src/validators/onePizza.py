def parse_input_file(file_lines):
  """
  Parse the input file and return the ingredients and clients.
  ingredients: list of ingredients
  clients: list of dictionaries with keys "likes" and "dislikes"
  """

  client_num = int(file_lines[0])
  ingredients = set()
  clients = list()

  for i in range(1, 2 * client_num, 2):

    line_likes = file_lines[i][:-1]
    line_dislikes = file_lines[i + 1][:-1]
    client_likes = line_likes.split(" ")[1:]
    client_dislikes = line_dislikes.split(" ")[1:]

    for item in set().union(client_likes, client_dislikes):
      ingredients.add(item)

    clients.append({
        "likes": client_likes,
        "dislikes": client_dislikes
    })

  return list(ingredients), clients


def parse_output_file(file_line) -> list:
  """
  Parse the output file and return the pizza.
  List of ingredients.
  """

  return file_line.split(" ")[1:]


def gets_point(ingredients, likes, dislikes):
  """
  Check if the pizza gets a point from a client.
  ingredients: list of ingredients in the solution pizza
  likes: list of ingredients the client likes
  dislikes: list of ingredients the client dislikes
  """

  return set(likes).issubset(ingredients) and not set(
      dislikes).intersection(ingredients)


def calculate_score(client_preferences, pizza):
  """
  Calculate the score of the pizza.
  client_preferences: list of dictionaries with keys "likes" and "dislikes"
  pizza: list of ingredients in the solution pizza
  """

  score = 0

  for client in client_preferences:
    if gets_point(pizza, client["likes"], client["dislikes"]):
      score += 1

  return score
