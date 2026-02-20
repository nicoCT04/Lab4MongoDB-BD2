# MongoDB Atlas Connection Guide (Python)

Esta guía explica cómo conectarse correctamente a un cluster de MongoDB Atlas desde cualquier máquina usando Python.

Incluye:

* Creación de entorno virtual
* Instalación de dependencias
* Configuración de variables de entorno
* Solución al error SSL `CERTIFICATE_VERIFY_FAILED`
* Configuración de IP en MongoDB Atlas

---

# Crear entorno virtual

En la carpeta del proyecto:

```bash
python3 -m venv venv
```

Activar el entorno virtual:

### Mac / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

# Instalar dependencias

Con el entorno virtual activado:

```bash
pip install --upgrade pip
pip install pymongo pandas python-dotenv certifi
```

`certifi` es IMPORTANTE para evitar errores SSL.

---

# 3️⃣ Configurar archivo .env

Crear un archivo llamado `.env` en la raíz del proyecto:

```
MONGO_URI=mongodb+srv://USUARIO:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
```

⚠️ No usar comillas
⚠️ No dejar espacios

---

# Código correcto para conexión segura

En tu archivo Python debes usar:

```python
import certifi
from pymongo import MongoClient

client = MongoClient(
    mongo_uri,
    tls=True,
    tlsCAFile=certifi.where()
)
```

Esto evita problemas de certificados SSL.

---

# ERROR COMÚN EN MAC: CERTIFICATE_VERIFY_FAILED

Si aparece este error:

```
SSL: CERTIFICATE_VERIFY_FAILED
```

Ejecutar en terminal:

```bash
/Applications/Python\ 3*/Install\ Certificates.command
```

O manualmente:

Finder → Applications → Python 3.x → Install Certificates.command
Hacer doble click.

Esto instala los certificados SSL necesarios.

---

### Para permitir cualquier IP (solo pruebas):

```
0.0.0.0/0
```

---

# 9️⃣ Comando final para ejecutar script

```bash
python3 csv_to_mongo.py data.csv lab4 cars
```

Donde:

* `data.csv` → archivo CSV
* `lab4` → base de datos
* `cars` → colección

MongoDB crea automáticamente la base de datos y colección si no existen.
