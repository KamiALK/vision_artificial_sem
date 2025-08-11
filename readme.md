# build
Se realiza el despliegue de la base de datos con docker,
y se realiza conexion a base de datos mysql.

como motor de manejo de consultas se usa dbeaver

al levantar los contenedores  el servicio web se accede en el puerto :8080

http://localhost:8080

se requiere para administrar sesion de la dbeaver 
usuario:   cbadmin
Passwaord: Admin1234


# crear conexion de mysql 


driver: mysql
host: mysql1
Port: 3306
Database:SolarInfo
Conenection name:  Vision
user name: root
User Passwaord: kamiloalca

configurar driver properties:
cambiar esta opcion a true
- allowPublicKeyRetrival True

## dependencias

```python


pip install sqlalchemy python-dotenv
```

mirar el ip del contenedor
```bash

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql1
```
