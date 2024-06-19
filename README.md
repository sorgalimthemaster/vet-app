# vet-app

#POSTGRESQL
Primero necesitas tener dos bases de datos en postgresql llamadas:
-> bdveterinaria
SCRIPTS DE LAS TABLAS:

-- Table: public.consulta

-- DROP TABLE IF EXISTS public.consulta;

CREATE TABLE IF NOT EXISTS public.consulta
(
    id integer NOT NULL DEFAULT nextval('consulta_id_seq'::regclass),
    id_mascota integer NOT NULL,
    consulta text COLLATE pg_catalog."default" NOT NULL,
    fecha date DEFAULT CURRENT_DATE,
    CONSTRAINT consulta_pkey PRIMARY KEY (id),
    CONSTRAINT consulta_id_mascota_fkey FOREIGN KEY (id_mascota)
        REFERENCES public.mascota (id_mascota) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.consulta
    OWNER to postgres;

-- Table: public.mascota

-- DROP TABLE IF EXISTS public.mascota;

CREATE TABLE IF NOT EXISTS public.mascota
(
    id_mascota integer NOT NULL DEFAULT nextval('mascota_id_mascota_seq'::regclass),
    id_propietario integer NOT NULL,
    nombre_mascota character varying(255) COLLATE pg_catalog."default" NOT NULL,
    raza character varying(255) COLLATE pg_catalog."default" NOT NULL,
    "año_nacimiento" integer NOT NULL,
    CONSTRAINT mascota_pkey PRIMARY KEY (id_mascota),
    CONSTRAINT mascota_id_propietario_fkey FOREIGN KEY (id_propietario)
        REFERENCES public.propietario (id_propietario) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.mascota
    OWNER to postgres;

-- Table: public.propietario

-- DROP TABLE IF EXISTS public.propietario;

CREATE TABLE IF NOT EXISTS public.propietario
(
    id_propietario integer NOT NULL DEFAULT nextval('propietario_id_propietario_seq'::regclass),
    nombre character varying(255) COLLATE pg_catalog."default" NOT NULL,
    apellidopat character varying(255) COLLATE pg_catalog."default" NOT NULL,
    apellidomat character varying(255) COLLATE pg_catalog."default" NOT NULL,
    telefono character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT propietario_pkey PRIMARY KEY (id_propietario)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.propietario
    OWNER to postgres;


-> login
SCRIPTS NECESARIOS:

-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    username character varying(50) COLLATE pg_catalog."default" NOT NULL,
    email character varying(100) COLLATE pg_catalog."default" NOT NULL,
    hashed_password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_username_key UNIQUE (username)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;


#EJECUCION PYTHON

- Crea un entorno virutal, lo puedes hacer con visual studio code.
- Recuerda tener instalado python 3.11.9
- Al estar creando el entorno virutal te pedira los requirements.txt, ya viene adjunto al proyeto.
- Una vez en el entorno virutal lo ejecutas así: python src/main.py

#CONFIGURACION BD EN PYTHON
Usuario:  postgres
Contraseña: root
Host: localhost
Puerto: 5432
Base de datos: login o bdveterinaria

- Estos datos son los que estan en el python ya configurados, por si ocupas hacer un cambió.
-> SQLALCHEMY_DATABASE_URL_LOGIN = "postgresql://postgres:root@localhost:5432/login"
-> SQLALCHEMY_DATABASE_URL_VETERINARIA = "postgresql://postgres:root@localhost:5432/bdveterinaria"
