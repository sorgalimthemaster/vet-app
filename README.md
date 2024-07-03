
# Vet-App

## PostgreSQL

Primero, necesitas tener dos bases de datos en PostgreSQL llamadas:
- `vetheart`

### Scripts de las Tablas

#### Tabla: `consulta`

```sql
-- DROP TABLE IF EXISTS consulta;

CREATE TABLE IF NOT EXISTS consulta (
    id SERIAL PRIMARY KEY,
    id_mascota INTEGER NOT NULL,
    consulta TEXT NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    CONSTRAINT consulta_id_mascota_fkey FOREIGN KEY (id_mascota)
        REFERENCES mascota (id_mascota)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
```

#### Tabla: `mascota`

```sql
-- DROP TABLE IF EXISTS mascota;

CREATE TABLE IF NOT EXISTS mascota (
    id_mascota SERIAL PRIMARY KEY,
    id_propietario INTEGER NOT NULL,
    nombre_mascota VARCHAR(255) NOT NULL,
    raza VARCHAR(255) NOT NULL,
    año_nacimiento INTEGER NOT NULL,
    CONSTRAINT mascota_id_propietario_fkey FOREIGN KEY (id_propietario)
        REFERENCES propietario (id_propietario)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);
```

#### Tabla: `propietario`

```sql
-- DROP TABLE IF EXISTS propietario;

CREATE TABLE IF NOT EXISTS propietario (
    id_propietario SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidopat VARCHAR(255) NOT NULL,
    apellidomat VARCHAR(255) NOT NULL,
    telefono VARCHAR(50) NOT NULL
);
```

#### Tabla: `users`

```sql
-- DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Ejecución de Python

1. Crea un entorno virtual. Puedes hacerlo con Visual Studio Code.
2. Asegúrate de tener instalado Python 3.12.4.
3. Al crear el entorno virtual, te pedirá los `requirements.txt`, ya incluido en el proyecto.
4. Una vez en el entorno virtual, ejecuta el proyecto con:
   ```bash
   python src/main.py
   ```

## Configuración de la Base de Datos en Python

- **Usuario:** `vetheart`
- **Contraseña:** `s7iCPaIFeF0SY8hCi3tyjy1FI5GKZBgm`
- **Host:** `dpg-cq2pq1qju9rs7391sgug-a.oregon-postgres.render.com`
- **Puerto:** `5432`
- **Bases de datos:** `vetheart`

Estos son los datos de conexión configurados en el archivo Python:

```python
SQLALCHEMY_DATABASE_URL_VETERINARIA = "postgresql://vetheart:s7iCPaIFeF0SY8hCi3tyjy1FI5GKZBgm@dpg-cq2pq1qju9rs7391sgug-a.oregon-postgres.render.com/vetheart"
```
