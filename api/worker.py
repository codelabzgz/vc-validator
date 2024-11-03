import cProfile
from datetime import datetime
from os import getenv as env

from fastapi import FastAPI, HTTPException, staticfiles

from models.req import EventData
from validators import fibonacci, onePizza, unicode24

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
async def validator_one_pizza(data: EventData):
    try:
        id = 0
        data.points = 0
        for file in data.files:
            filename = file.filename
            content = file.content

            # procesa el archivo base con el que se compara la entrada del usuario
            with open(f'api/static/one-pizza/{filename}', 'r', encoding='utf-8') as f:
                infile_content = f.readlines()
                _, clients = onePizza.parse_input_file(infile_content)
            
            # Procesa el archivo subido (outfile).
            pizza = onePizza.parse_output_file(content)

            score = onePizza.calculate_score(clients, pizza)
            print(score)

            data.points = max(data.points, score)
            file.tests.append({
                "id": id + 1,
                "input": {
                    "file": {
                        "name": filename,
                        "path": f"{env("API_URL")}/static/one-pizza/{filename}",
                    }
                },
                "actual": content,
                "success": score > 0,
                "points": score
            })
            id += 1

        return data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


@app.post("/validator/fibonacci")
async def validator_fibonacci(data: EventData):
    try:
        for test in data.files[0].tests:
            outputs = [int(x) for x in test.actual.split(", ")]
            success = fibonacci.is_fibonacci_sequence(outputs)
            test.success = success
            test.actual = test.output.stdout
            test.points = 5 if success else 0

        return data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )

@app.post("/validator/unicode-24")
async def validator_unicode24(data: EventData):
    try:
        filename = data.files[0].filename
        level = 1
        match data.difficulty:
            case 'medium':
                level = 2 
            case 'hard' | 'insane':
                level = 3 
        config = unicode24.MapConfig(f"api/static/unicode-24/{filename}", level)
        scoring_param, err = unicode24.validate_output(config, data.files[0].content)
        data.files[0].tests[0] = {
            "id": 1,
            "input": {
                "file": {
                    "name": filename,
                    "path": f"{env("API_URL")}/static/unicode-24/{filename}",
                }
            },
            "actual": err,
            "success": err is None,
            "points": 0 if err is not None else unicode24.score(scoring_param, ds_size, level) 
        }
        return data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
