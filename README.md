# vc-validator

[![python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org)
[![pip](https://img.shields.io/badge/pip-24-0-blue)](https://pypi.org/project/pip)

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![FastAPI Badge](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=for-the-badge)
![Pydantic Badge](https://img.shields.io/badge/Pydantic-E92063?logo=pydantic&logoColor=fff&style=for-the-badge)
![Vercel Badge](https://img.shields.io/badge/Vercel-000?logo=vercel&logoColor=fff&style=for-the-badge)

Este proyecto ofrece una plantilla para crear un validador de retos con FastAPI.

## Creación del Validador

> [!NOTE] Para ejecutar y desplegar tu proyecto en Vercel, necesitas tener instalada la CLI de Vercel. Puedes instalarla globalmente usando npm: `npm install -g vercel`

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

Para ejecutar el servidor localmente, utiliza el siguiente comando:

```bash
vercel dev
```

### Despliegue en Vercel

Para desplegar tu proyecto en Vercel, puedes hacerlo de dos maneras:

1. **Automáticamente**: Realiza un commit en tu repositorio, y las acciones de GitHub se encargarán del despliegue.
2. **Manualmente**: Ejecuta el siguiente comando:

```bash
vercel --prod
```

---

## Despliegue de Judge0 On-Premise

| Acción | Comando |
| --- | --- |
| Iniciar el servicio	| `make start` |
| Detener el servicio	| `make stop` |