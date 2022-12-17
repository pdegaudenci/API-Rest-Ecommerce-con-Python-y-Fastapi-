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

__Externalización de datos sensibles : datos conexión BBDD y de autenticación de la API__

* Crear un archivo `.env`, donde se declaran e inicializan las variables de entorno de usuaruis individuales que son usadas durante el ciclo de ejecución de la API. 

Los siguientes parámetros con necesarios para acceder a la conexión entre el API rest y la base de datos PostgreSQL:

```
Da un ejemplo
```

_Y repite_

```
hasta finalizar
```

_Finaliza con un ejemplo de cómo obtener datos del sistema o como usarlos para una pequeña demo_

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

_Agrega notas adicionales sobre como hacer deploy_

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - El framework web usado
* [Maven](https://maven.apache.org/) - Manejador de dependencias
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).


## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

