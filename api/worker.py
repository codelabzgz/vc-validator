from fastapi import FastAPI, File, UploadFile, HTTPException, staticfiles
from datetime import datetime
from validators import onePizza
from pydantic import BaseModel, HttpUrl
from typing import Dict
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()


class InputFile(BaseModel):
  name: str
  path: HttpUrl


class ValidatorOnePizzaResponse(BaseModel):
  id: str
  input: Dict[str, InputFile]
  success: bool
  points: int


app = FastAPI()
app.mount(
    "/static",
    staticfiles.StaticFiles(directory="src/static"),
    name="static"
)


@app.get("/health")
async def health_check():
  """
  Endpoint de verificación del estado de la API.
  Devuelve la fecha y hora actuales para confirmar que la API está funcionando.
  """
  return {
      "status": {
          "timestamp": datetime.now().isoformat()
      }
  }

# Endpoint de validación específico para el evento "one-pizza"


@app.post("/validator/one-pizza", response_model=ValidatorOnePizzaResponse)
async def validator_one_pizza(outfile: UploadFile = File(...)):
  """
  Endpoint para validar el archivo de salida de un problema de ejemplo ("one-pizza").

  Parámetros:
  - outfile (UploadFile): Archivo subido que debe ser validado.

  Funcionamiento:
  1. Lee el contenido del archivo de entrada predefinido (infile) desde la ruta especificada.
  2. Usa la función parse_input_file del módulo `onePizza` para procesar el contenido del archivo de entrada.
  3. Lee el contenido del archivo subido (`outfile`), lo decodifica y lo convierte en una lista de líneas.
  4. Usa la función parse_output_file del módulo `onePizza` para procesar el contenido del archivo subido.
  5. Calcula la puntuación usando la función `calculate_score` del módulo `onePizza`.
  6. Devuelve un resultado que incluye un identificador, un estado de éxito y la puntuación calculada.

  Devuelve:
  - Un diccionario con el resultado de la validación que incluye:
      - 'id': Identificador del evento o archivo.
      - 'input': Ejemplo de entrada (puede ser ajustado según el contexto real).
      - 'success': Booleano que indica si la puntuación es mayor que 0.
      - 'points': La puntuación calculada.

  Manejo de Errores:
  - Si ocurre un error durante el procesamiento, se captura y se devuelve un error 500 con un mensaje descriptivo.
  """
  try:
    # procesa el archivo base con el que se compara la entrada del usuario
    filename = 'a_an_example.in.txt'
    with open(f'src/static/{filename}', 'r', encoding='utf-8') as f:
      infile_content = f.read()
      _, clients = onePizza.parse_input_file(infile_content)

    # Procesa el archivo subido (outfile).
    outfile_content = await outfile.read()
    outfile_content = outfile_content.decode("utf-8")
    pizza = onePizza.parse_output_file(outfile_content)

    score = onePizza.calculate_score(clients, pizza)

    return ValidatorOnePizzaResponse(
        id='one-pizza',
        input={
            'file': InputFile(
                name=filename,
                path=f'{env("API_URL")}/static/{filename}'
            )
        },
        success=score > 0,
        points=score
    )

  except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Internal Server Error: {str(e)}"
    )
