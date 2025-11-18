# SIGEU_2 – Sistema de Gestión de Eventos Universitarios  
### Base de Datos Documental – Tercera Entrega

Este documento corresponde a la **Tercera Entrega – Base de Datos Documental** del proyecto SIGEU_2.  
Incluye modelado, creación de BD, triggers, carga de datos, backend FastAPI y pruebas en Swagger y Postman.

---

## 1️⃣ Descripción del Proyecto

SIGEU_2 es un Sistema Documental para la gestión de eventos académicos usando:

- MongoDB (documental)
- FastAPI (backend)
- Motor (AsyncIOMotorClient)
- Hackolade (modelado)
- Postman (pruebas)
- Swagger (documentación)

El sistema administra:

- Usuarios
- Facultades
- Unidades académicas
- Programas
- Eventos
- Organizaciones externas
- Participación y evaluación de eventos

---

## 2️⃣ Integrantes

| Integrante | Código |
|-----------|--------|
| Rodrigo Andrés Gómez López | 2247014 |
| David Hernández Paz | 2247003 |
| Daniel Alexander Brand García | 2246133 |
| Sebastián Manrique Mejía | 2246988 |
| Michael Macowli Cardona Rodríguez | 2246268 |

Docente: **PhD. Jhon Eder Masso Daza**

---

## 3️⃣ Modelado en Hackolade

Archivos:

```
docs/MODELADO/
│── SIGEU_2_Hackolade_andres_nov.hck.json
│── SIGEU_2_DOCUMENTACION_MODELADO_Hackolade.pdf
```

Incluye:

- Colecciones
- Relaciones por referencias
- `$jsonSchema`
- Índices
- Validaciones documentales

Abrir con Hackolade:

```
File → Open → SIGEU_2_Hackolade_andres_nov.hck.json
```

---

## 4️⃣ Creación de la BD en MongoDB

En MongoDB Compass → Shell:

```js
use('sigeu_2');
load('sigeu_2_PARA_MONGO.txt');
```

El script crea:

- Colecciones
- Validadores `$jsonSchema`
- Índices
- Reglas de negocio básicas

---

## 5️⃣ Emulación de Triggers en MongoDB

Triggers emulados mediante JavaScript:

| Función | Propósito |
|--------|-----------|
| crearUsuario() | Valida dominio y rol |
| asignarUsuarioAPrograma() | Solo estudiantes pueden ingresar |
| registrarOrganizadorEvento() | Solo docentes/estudiantes organizan |
| evaluarEvento() | Solo secretarios evalúan |

Ejecutar:

```js
load('sigeu_2_triggers.js');
```

Validar:

```js
typeof crearUsuario
typeof asignarUsuarioAPrograma
typeof registrarOrganizadorEvento
typeof evaluarEvento
```

---

## 6️⃣ Carga de Datos de Prueba

Ejecutar:

```js
load('sigeu_2_datos_prueba.js');
```

Verificar:

```js
[
 'facultad','unidad_academica','programa_academico','usuario','lugar',
 'evento','organizacion_externa','programa_usuario','unidad_usuario',
 'facultad_usuario','usuario_organizador','lugar_evento','participa','evaluacion_evento'
].forEach(c => print(c,':',db.getCollection(c).countDocuments()));
```

Limpiar (si es necesario):

```js
db.usuario.deleteMany({});
db.evento.deleteMany({});
...
```

---

## 7️⃣ Backend FastAPI

Estructura:

```
SIGEU_2_MONGO/
│── docs/
│── .env
│── requirements.txt
└── src/
    ├── main.py
    ├── db/
    ├── models/
    ├── crud/
    └── routes/
```

###  Conexión a MongoDB (client.py)

```python
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
```

###  Modelos Pydantic

Incluye validaciones de:

- correo UAO
- roles permitidos
- ObjectId
- fechas

###  CRUD

- usuario_crud.py  
- facultad_crud.py  
- unidad_academica_crud.py  
- evento_crud.py  
- organizacion_externa_crud.py  

###  Rutas

- /usuarios  
- /facultad  
- /unidad-academica  
- /programa-academico  
- /lugar  
- /eventos  
- /organizacion-externa  

---

## 8️⃣ Ejecución del Backend

### Crear entorno virtual

```bash
py -3.11 -m venv sigeu2_venv
sigeu2_venv\Scriptsctivate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
pip install email-validator
```

### Archivo `.env`

```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=sigeu_2
```

### Ejecutar FastAPI

```bash
uvicorn src.main:app --reload
```

---

## 9️⃣ Pruebas en Swagger

Abrir:

 http://127.0.0.1:8000/docs

### Ejemplo crear evento

```json
{
  "nombre": "Foro de Innovación en Ingeniería",
  "descripcion": "Evento de prueba",
  "fecha_inicio": "2025-03-20T09:00:00",
  "fecha_fin": "2025-03-20T12:00:00",
  "lugar_id": "691ba800c3779517a9735276",
  "facultad_id": "691ba800c3779517a9735241",
  "unidad_academica_id": "691ba800c3779517a9735243",
  "programa_academico_id": "691ba800c3779517a9735246",
  "organizacion_externa_id": "691ba800c3779517a973528a"
}
```

---

## 🔟 Pruebas en Postman

Archivo incluido:

```
SIGEU_2_Mongo_Seeds.postman_collection.json
```

Seleccionar environment:

```
SIGEU - Localhost
baseUrl = http://127.0.0.1:8000
```

Seeds disponibles:

- facultad  
- unidad_academica  
- programa_academico  
- contrasena  
- evaluacion_evento  
- facultad_usuario  
- unidad_usuario  
- programa_usuario  
- lugar  
- lugar_evento  
- organizacion_externa  
- participa  
- usuario_organizador  

---

## 1️⃣1️⃣ Enlaces Importantes

### GitHub Backend  
https://github.com/aglsystems-ragl/SIGEU_2_MONGO.git

### Postman  
https://andresgomezdoctorado-8529723.postman.co/workspace/andres-gomez's-Workspace~25a1ed28-155c-4f0f-8243-ddf433ed08ec/collection/49033182-aac2ae40-a91f-440d-a8c1-c7774f89d74d

---

## 1️⃣2️⃣ Créditos

Proyecto académico desarrollado para la asignatura **Almacenamiento de Datos**  
Universidad Autónoma de Occidente — 2025  
Uso estrictamente educativo.
