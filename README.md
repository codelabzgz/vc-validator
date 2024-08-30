# vc-validator

Este proyecto ofrece una plantilla para crear un validador de retos con FastAPI.

## Creación del Validador

### Instalación de Dependencias

1. **Clona el repositorio**:

```bash
git clone -b develop --depth 1 https://github.com/CodeLabZGZ/cf-validator.git
```

2. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

3. **Guarda las dependencias** (si realizaste cambios):
```bash
pip freeze > requirements.txt
```

### Ejecutar el Servidor

- **Con `fastapi`**:

```bash
fastapi dev src/worker.py
```

- **Con `uvicorn`**:

```bash
uvicorn src.worker:app --reload
```

## Despliegue en Vercel

Por escribir...

---

## Despliegue de Judge0 On-Premise

Por escribir...
