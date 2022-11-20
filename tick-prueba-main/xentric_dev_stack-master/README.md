# xentric_dev_stack

Stack con lo necesario para levantar los contenedores base de la aplicación. En principio, Keycloak (Postgres) y Mongo

Para ejecutar:
'''
docker-compose up -d
'''
# Importar recursos y scopes

Para que funcione correctamente hay que importar los recursos que esta en formato json del directorio auths e ingresarlos en

- Realm : Alloxentric
- Clients
- xentric_base
- Authorization
- Import