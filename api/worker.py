from fastapi import FastAPI, HTTPException, staticfiles
from datetime import datetime
from validators import onePizza, fibonacci
from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class InputFile(BaseModel):
    name: str
    path: HttpUrl


class RequestData(BaseModel):
    id: str
    event: str
    challenge: str
    input: Optional[str] = None
    expected: Optional[str] = None
    outputs: str


app = FastAPI()
app.mount(
    "/static",
    staticfiles.StaticFiles(directory="api/static"),
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


@app.post("/validator/one-pizza")
async def validator_one_pizza(data: List[RequestData]):
    try:
        for test in data:
            filename = test.input
            content = test.outputs
            print(test)

            # procesa el archivo base con el que se compara la entrada del usuario
            with open(f'api/static/{filename}', 'r', encoding='utf-8') as f:
                infile_content = f.read()
                _, clients = onePizza.parse_input_file(infile_content)

            # Procesa el archivo subido (outfile).
            pizza = onePizza.parse_output_file(content)

            score = onePizza.calculate_score(clients, pizza)
            print(score)

        return data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


@app.post("/validator/fibonacci")
async def validator_one_pizza(data: List[RequestData]):
    try:
        response = []
        for test in data:
            print(test)
            outputs = [int(x) for x in test.outputs.split(", ")]
            success = fibonacci.is_fibonacci_sequence(outputs)
            print(success)

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
