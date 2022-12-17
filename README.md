# API Rest E-Commerce Project
![SharedScreenshot](https://user-images.githubusercontent.com/73450522/208239577-ff8471d0-b196-4c86-80a5-76c1c41a8731.jpg)

_Aplicación que proporciona soporte tecnológico para los procesos de negocios de ventas y gestion de inventario de una tienda de venta minorista de móviles, construida con un modelo de interfaz tipo API Rest y un modelo de datos relacional en una Base de Datos PostgreSQL como servicio externo.
El sistema de autenticacion se basa en el estándar OAUTH2, utilizando tokens como medio de autenticación y perfiles de usuario para el control de acceso a determinados recursos / operaciones de la API.
El proyecto fue realizado con el framework FastApi (Python), usando el ORM (Object Relationship Mapping) SQLAlchemy para el mapeo de las entidades logicas en codigo Python a las entidades del modelo relacional y viceversa_

![Explicacion_api](https://user-images.githubusercontent.com/73450522/208242357-f6cc8dc7-c883-4b67-879d-e6ffe0b30447.jpg)

## Comenzando (Desde terminal bash o cmd de Windows)🚀

_Clonar el proyecto a nivel local._

```
git clone https://github.com/pdegaudenci/APIRest-Ecommerce.git
```

_Movernos a la ubicacion del directorio raiz del proyecto_

```
cd APIRest-Ecommerce
```

### Pre-requisitos 📋

_La API Rest fue desarrollada con la version 3.10.7 de Python. Para entornos de prueba es necesario descargarla a través del siguiente enlace:_

* [Descarga oficial de Python 3.10.7](https://www.python.org/downloads/release/python-3107) 


_Una vez instalado Python 3, desde la terminal --> instalar las dependencias del proyecto necesarias mediante el gestor de paquetes nativo de Python `pip`_

```
pip install -r requirements.txt
```

_La API Rest interactua, intercambiando informacion, con un servicio externo, que es un Servidor de BBDD relacional PostgreSQL . Por lo tanto será necesario contar con un motor de BBDD igual o similar montado en un servidor o localmente, con el cual la API pueda realizar las operaciones de consulta y modificaciòn de datos. En la seccion de Instalacion se indica los pasos a seguir en caso de que se desee usar un motor de BBDD relacional distinto_

* [Descarga PostgreSql](https://www.postgresql.org/download/)

### Instalación 🔧

__Creación de la Base de datos a usar por la API con un cliente como PgAdmin__

__Externalización de datos sensibles : datos conexión BBDD y de autenticación de la API__

* Moverse  la carpeta `config/` del proyecto y crear un archivo `.env`, donde se declaran e inicializan las variables de entorno de usuaruis individuales que son usadas durante el ciclo de ejecución de la API. Las variables de entorno contienen los parametros necesarios para la  conexion entre la API y la BBDD, ademas de ciertos valores utilizados en el sistema de generación de tokens.

* Variables de entorno de la aplicación:

| Variable de entorno              | Descripción                                                                   |       Ejemplo                      |
|----------------------------------|-------------------------------------------------------------------------------|------------------------------------|
| `USER`                           | Username de la BBDD                                                           | `postgres`                         |
| `PASSWORD`                       | Contraseña de la BBDD                                                         | `postgres1234`                     |
| `HOST`                           | URL o IP del Server de BBDD                                                   | `localhost`                        |
| `PORT`                           | Puerto de escucha del server de BBDD                                          | `5432`                             |
| `DATABASE`                       | Nombre de la BBDD creado previamente                                          | `e-commerce`                       |
| `ADMIN`                          | Usuario admin creado por defecto al iniciar por 1º vez la API                 | `admin`                            |
| `PASSWORD_ADMIN`                 | Contraseña de user admin                                                      | `adminPasswword`                   |
| `SECRET_KEY`                     | Cadena utilizada en la generación del token de autenticación(CSRF Protection) |                                    |
| `ACCESS_TOKEN_EXPIRE_MINUTE`     | Tiempo en minutos del periodo de validez de los token                         | `60` --> tiempo de validez: 1 hora |

* Ejemplo de archivo `.env`:

![config](https://user-images.githubusercontent.com/73450522/208251275-7066fdb2-3d66-40c6-97e3-7381fbce5912.jpg)


## Ejecutando las pruebas ⚙️

_Explica como ejecutar las pruebas automatizadas para este sistema_

### Analice las pruebas end-to-end 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

### Y las pruebas de estilo de codificación ⌨️

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

## Despliegue 📦

_Ejecutar el servidor web liviano ASGI `uvicorn` desde la terminal en la raíz del proyecto_
```
uvicorn app:app --reload
```

_ si se ejecuto de forma local correctamente :_

![dev](https://user-images.githubusercontent.com/73450522/208251741-d3cd96dc-f4ab-460b-be71-61ea865008e1.jpg)

## Construido con 🛠️

_Tecnologías usadas en este proyecto_

* [FastAPI](https://fastapi.tiangolo.com) - Framework  de python
* [Python 3](https://docs.python.org/3/) - Lenguaje de programación
* [pip](https://pip.pypa.io/en/stable/) - gestor de dependencias
* [SQLAlchemy](https://www.sqlalchemy.org) - ORM usado para el mapeo de las entidades python al modelo relacional. El driver o conector para PostgreSQL usado es [psycopg2](https://pypi.org/project/psycopg2/)
* [Pydantic](https://docs.pydantic.dev) - Libreria para las validaciones de los requests mediante el uso de dataclass en Python para definir esquemas de validación.
* [Python dotenv](https://pypi.org/project/python-dotenv/) - Libreria para generar y configurar archivos de entorno y poder leer las variables de entorno que almacenan.
* [Pytest](https://docs.pytest.org/en/7.2.x/) - Libreria usada oara crear las pruebas unitarias durante la fase de testing de funcionalidades.
* OAUTH2 -  Estándar framework de autorización para la gestión de las autenticaciones de las requests de usuarios.
* [Json Web Token (JWT)](https://jwt.io) - Estandar para la generacion e encriptación de los tokens de autenticación del usuario 
* Logging - libreria para la generacion de registros de ocurrencias (logger) ante determinados eventos de la API Rest


## Datos del proyecto 📖

El proyecto se realizó bajo un enfoque Agile, organizado en 2 sprints de 10 dias cada uno. Se completaron las siguientes fases del ciclo de desarrollo de SW:

![Explicacion_api (2)](https://user-images.githubusercontent.com/73450522/208253273-5844fd1e-e6aa-4b99-92b0-8831926ce6d2.jpg)

* El modelo de datos definido es el siguiente:

[Database ER diagram (E-commerce API ) (2).pdf](https://github.com/pdegaudenci/APIRest-Ecommerce/files/10252235/Database.ER.diagram.E-commerce.API.2.pdf)

El diseño de la aplicación se hizo siguiendo una arquitectura por capas , con capas independientes e interconectadas, segun el siguiente detalle de estructura de proyecto:

  ![EstructuraCarpetas](https://user-images.githubusercontent.com/73450522/208253917-c44feac7-39f1-4bbc-8df8-7f2a784fb9ae.jpg)


* Carpeta Config: Se crea la conexión y enlace con la BBDD a traves del engine de SQLAlchemy
* Carpeta models: declaracion de las clases o entidades en Python que heredan de la clase Base de SQLAlchemy a fin de que posteriormente sean mapeadas a la Base de Datos relacional (Atributos y relaciones). Cada clase se corresponde con una tabla.
* Carpeta schemas: Contiene las dataclass correspondiente a los esquemas de validacion (Esquemas de usuario , autenticacion , productos y pedidos) , las cuales herdan de la clase BaseModel de Pydantic.
* Carpeta services: Contiene la logica de negocio y agrupa funcionalidades por entidades de negocio: autenticacion, usuarios, productos y pedidos. Establece la comunicacion bidireccional con la BBDD, realizando consultas , modificacion y procesamiento de datos para devolver a los metodos de la capa de enrutado.
* Carpeta router: Sistema de enrutado de la API, que contiene los metodos que gestionarán las peticiones recibidas a cada uno de los endpoints soportados por la aplicación. Las funcionalidades u operaciones permitidas por la API se agrupan por entidades de datos. Existen rutas para gestion de inventarios, gestion de usuarios, autenticacion y gestion de pedidos y clientes.
* Carpeta test: Conjunto de pruebas unitarias realizadas a los endpoints de la API a través de la libreria PyTest.
* Carpeta utils: conjunto de metodos auxiliares de la aplicacion que contiene dos funcionalidades: logging y carga de datos tabulares (excel o csv) en las tablas correspondientes de la BBDD

Para mas informacion de la etapa de desarrollo del proyecto :[Flujo de trabajo del proyecto]([./workflow del proyecto.txt](https://github.com/pdegaudenci/APIRest-Ecommerce/blob/developer/workflow%20del%20proyecto.txt))

## Licencia 📄

Este proyecto está bajo la Licencia Licencia pública general de GNU v2.0 (gpl-2.0)
