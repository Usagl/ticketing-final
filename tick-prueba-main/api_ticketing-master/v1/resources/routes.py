# obtenemos la clase del recurso que tenemos en el archivo example.py para utilizarlo en un endpoint
#from v1.resources.example.example import Role
from v1.resources.methods.pymongo import EndPoint1, EndPoint2, EndPoint3
from v1.resources.methods.Crud_methods import ticket_GETALL, ticket_CRUD, ticketStatus, returnSystemTicket

def initialize_routes(api):
    '''
    En el endpoint le indicamos el recurso keycloak a utilizar
    con el formato "auth:nombrerecurso:explicacion_corta"
    '''
    #api.add_resource(Role, '/role', endpoint='auth:flask_base:dev', methods=['GET','POST',])
    api.add_resource(ticket_GETALL, '/list', endpoint='auth:recurso5', methods=['GET','POST']) # <--- Permite listar
    api.add_resource(ticket_CRUD, '/audit_ticket', endpoint='auth:recurso4', methods=['GET', 'POST', 'PUT', 'DELETE']) # <--- Permite ejecutar metodos CRUD
    api.add_resource(ticketStatus, '/status', endpoint='auth:recurso6', methods=['GET','POST', 'PUT']) # <--- Permite cambiar el status del ticket
    api.add_resource(returnSystemTicket, '/ticket', endpoint='auth:recurso3', methods=['GET','POST']) # <--- traer tickets de cada sistema
