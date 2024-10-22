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


unicode24_easy_ds = unicode24.MapConfig("api/static/unicode24_facil.txt", 1)
unicode24_medium_ds = unicode24.MapConfig("api/static/unicode24_medio.txt", 2)
unicode24_hard_ds = unicode24.MapConfig("api/static/unicode24_dificil.txt", 3)

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
            with open(f'api/static/{filename}', 'r', encoding='utf-8') as f:
                infile_content = f.readlines()
                _, clients = onePizza.parse_input_file(infile_content)
            
            # Procesa el archivo subido (outfile).
            pizza = onePizza.parse_output_file(content)

            score = onePizza.calculate_score(clients, pizza)

            data.points = max(data.points, score)
            file.tests.append({
                "id": id + 1,
                "input": {
                    "file": {
                        "name": filename,
                        "path": f"{env("API_URL")}/static/{filename}",
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

@app.post("/validator/unicode24")
async def validator_unicode24(data: EventData):
    match data.difficulty:
        case 'easy' | 'very easy': 
            config = unicode24_easy_ds 
        case 'medium':
            config = unicode24_medium_ds 
        case 'hard' | 'insane':
            config = unicode24_hard_ds 
    scoring_param, err = unicode24.validate_output(config, data.files[0].content) 
    data.files[0].tests[0].success = err is None 
    data.files[0].tests[0].points = 0 if err is not None else unicode24.score(scoring_param) 
    return data
