
# Vet-App

## PostgreSQL

Primero, necesitas tener dos bases de datos en PostgreSQL llamadas:
- `bdveterinaria`
- `login`

### Scripts de las Tablas

#### Tabla: `consulta`

```sql
-- DROP TABLE IF EXISTS public.consulta;

CREATE TABLE IF NOT EXISTS public.consulta (
    id SERIAL PRIMARY KEY,
    id_mascota INTEGER NOT NULL,
    consulta TEXT NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    CONSTRAINT consulta_id_mascota_fkey FOREIGN KEY (id_mascota)
        REFERENCES public.mascota (id_mascota)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE IF EXISTS public.consulta OWNER TO postgres;
```

#### Tabla: `mascota`

```sql
-- DROP TABLE IF EXISTS public.mascota;

CREATE TABLE IF NOT EXISTS public.mascota (
    id_mascota SERIAL PRIMARY KEY,
    id_propietario INTEGER NOT NULL,
    nombre_mascota VARCHAR(255) NOT NULL,
    raza VARCHAR(255) NOT NULL,
    año_nacimiento INTEGER NOT NULL,
    CONSTRAINT mascota_id_propietario_fkey FOREIGN KEY (id_propietario)
        REFERENCES public.propietario (id_propietario)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE IF EXISTS public.mascota OWNER TO postgres;
```

#### Tabla: `propietario`

```sql
-- DROP TABLE IF EXISTS public.propietario;

CREATE TABLE IF NOT EXISTS public.propietario (
    id_propietario SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidopat VARCHAR(255) NOT NULL,
    apellidomat VARCHAR(255) NOT NULL,
    telefono VARCHAR(50) NOT NULL
);

ALTER TABLE IF EXISTS public.propietario OWNER TO postgres;
```

#### Tabla: `users`

```sql
-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE IF EXISTS public.users OWNER TO postgres;
```

## Ejecución de Python

1. Crea un entorno virtual. Puedes hacerlo con Visual Studio Code.
2. Asegúrate de tener instalado Python 3.11.9.
3. Al crear el entorno virtual, te pedirá los `requirements.txt`, ya incluido en el proyecto.
4. Una vez en el entorno virtual, ejecuta el proyecto con:
   ```bash
   python src/main.py
   ```

## Configuración de la Base de Datos en Python

- **Usuario:** `postgres`
- **Contraseña:** `root`
- **Host:** `localhost`
- **Puerto:** `5432`
- **Bases de datos:** `login` o `bdveterinaria`

Estos son los datos de conexión configurados en el archivo Python:

```python
SQLALCHEMY_DATABASE_URL_LOGIN = "postgresql://postgres:root@localhost:5432/login"
SQLALCHEMY_DATABASE_URL_VETERINARIA = "postgresql://postgres:root@localhost:5432/bdveterinaria"
```
