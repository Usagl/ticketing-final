# pylint: disable=invalid-name
# pylint: disable=line-too-long
#imports python base
import logging
#import terceros
from flask import session, jsonify, json
from flask_restful import Resource, reqparse
from mongoengine.context_managers import switch_db

####################################################
#                   ZENDESK                        #
from zenpy import Zenpy                            #
from zenpy.lib.api_objects import Ticket, User     #
from zenpy.lib.api_objects import Comment          #
#                                                  #
####################################################

#####################################
#            FRESHDESK              #
from freshdesk.api import API       # 
#                                   #
#####################################

#Import del sistema
from v1.resources.auth.authorization import Auth
from v1.resources.auth.dbDecorator import dbAccess
from v1.models.api_models import ModelTicketAudit

#################################################################################################
#                                         FRESHDESK                                             #
credfresh = API('notengoempresa2.freshdesk.com', 'Ma10J4OdXLs8A0o2Ykpz')                        #
#                                                                                               #
#################################################################################################

########################################
#                ZENDESK               #
creds = {'email' : 'contacto@bnet.cl', #
        'password' : 'lj37hcw2',       #
        'subdomain': 'bnet6753'        #
 }                                     #
#                                      #
# Default                              #
zenpy_client = Zenpy(**creds)          #
#                                      #
########################################

logger = logging.getLogger(__name__)


#####################################################################
# Esta clase trae todos los registros que se encuentren en mongoDB  #
#####################################################################

class ticket_GETALL(Resource):
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):
        with switch_db(ModelTicketAudit, session["dbMongoEngine"]): 
            my_model = ModelTicketAudit.objects()    # <----- Trae todos los documentos de la BD                 
            if my_model:
                return jsonify(my_model.to_json())
        return "Objeto no encontrado", 400

###############################################################################
# Esta clase permite crear ticket y poder comentarlo en el respectivo sistema #
###############################################################################

class ticket_CRUD(Resource):
    
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("Sistema", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")         #----|
        parser.add_argument("Requester", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")       #----|
        parser.add_argument("Email", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")           #----|------ Campos obligatorios para la creación de un ticket.
        parser.add_argument("Subject", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")         #----|
        parser.add_argument("Description", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")     #----|
        parser.add_argument("Status", type=str, required=False, help="Mensaje que devolvera en caso de parametro mal ingresado")         #----|
        data = parser.parse_args()
        #Se de realizar un If en el cual se consulte el sistema que se le consultara al Model si existe y dependiendo del sistema entrara a la API respectiva.
        if data['Sistema'] == 'Zendesk':
            try:
                with switch_db(ModelTicketAudit, session["dbMongoEngine"]) as my_collection:
                    my_model = my_collection(Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description'], Status=data['Status'])
                    # creds = json.loads(session["user"]["ticketSystemAttr"])                          
                    # zenpy_client = Zenpy(**creds)
                    #Va permitir crear el ticket y obtener el ID de cada ticket.    
                    ticket_audit = zenpy_client.tickets.create(Ticket(requester=User(name=my_model.Requester, email=my_model.Email),subject=my_model.Subject, description=my_model.Description))
                    #Permite consultar el ID del ticket creado y almacenarlo dentro del documento.
                    my_model = my_collection(Id=ticket_audit.ticket.id,Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description'], Status=ticket_audit.ticket.status)
                    my_model.save()
            except Exception as err:
                logger.error(err)
            return jsonify(my_model.to_json())
        elif data['Sistema'] == 'Freshdesk':
            try:
                with switch_db(ModelTicketAudit, session["dbMongoEngine"]) as my_collection:
                    my_model = my_collection(Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description'], Status=data['Status'])
                    # creds = json.loads(session["user"]["ticketSystemAttr"])  
                    # credfresh = API(**creds)   
                    freshticket = credfresh.tickets.create_ticket(my_model.Subject,name=my_model.Requester , email=my_model.Email, description=my_model.Description)
                    my_model = my_collection(Id=freshticket.id, Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description'], Status=freshticket.status)
                    my_model.save()
            except Exception as err:
                logger.error(err)
            return jsonify(my_model.to_json())
        #elif data['Sistema'] == 'SISTEMA_MODEL':   <--- Aqui deberian poner el nuevo sistema.
        #   with switch_db(ModelTicketAudit, session["dbMongoEngine"]) as my_collection: <--- NO SE CAMBIA
        #   my_model = my_collection(Sistema=data['Sistema'], Requester=data['Requester'], Email=data['Email'], Subject=data['Subject'], Description=data['Description']) <--- NO SE CAMBIA
        else:
            logger.error(err)
        
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self): #Se ejecutara este metodo con el metodo post del endpoint.
        parser = reqparse.RequestParser() #Creamos un objeto para obtener los datos de la request.
        parser.add_argument("Sistema", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Id")
        parser.add_argument("Comment1", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #Obtenemos los datos de la request.
        #Se de realizar un If en el cual se consulte el sistema que se le consultara al Model si existe y dependiendo del sistema entrara a la API respectiva.
        if data['Sistema'] == 'Zendesk':
            with switch_db(ModelTicketAudit, session["dbMongoEngine"]):
                my_model = ModelTicketAudit.objects(Id=data['Id']).first() # <--- Buscara en los documentos el id y el sistema enviado por el front end.
                my_model.Comment1 = data['Comment1']
                # creds = json.loads(session["user"]["ticketSystemAttr"])                          
                # zenpy_client = Zenpy(**creds)
                ticket = zenpy_client.tickets(id=my_model.Id)
                ticket.comment = Comment(body=my_model.Comment1,public=False) # <--- Ingresara el comentario del front-end.
                zenpy_client.tickets.update(ticket) # <--- Con los parametros de ID y Comentario se actualizara el ticket.
                my_model.save()
            return jsonify(my_model.to_json())
        elif data['Sistema'] == 'Freshdesk':
            with switch_db(ModelTicketAudit, session["dbMongoEngine"]):
                my_model = ModelTicketAudit.objects(Id=data['Id']).first()
                my_model.Comment1 = data['Comment1']
                # creds = json.loads(session["user"]["ticketSystemAttr"])  
                # credfresh = API(**creds) 
                credfresh.comments.create_note(ticket_id=my_model.Id, body=my_model.Comment1, private=False)
                my_model.save()
            return jsonify(my_model.to_json())
        # elif data['Sistema'] == 'NUEVO_SISTEMA':         <--- Aqui deberian poner el nuevo sistema.
        #     with switch_db(ModelTicketAudit, session["dbMongoEngine"]): <--- NO SE CAMBIA
        #         my_model = ModelTicketAudit.objects(Id=data['Id']).first() <--- NO SE CAMBIA
        #         my_model.Comment1 = data['Comment1']   <--- NO SE CAMBIA  
        else:
            print("No sistema")

class ticketStatus(Resource):

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self): #Se ejecutara este metodo con el metodo post del endpoint.
        parser = reqparse.RequestParser() #Creamos un objeto para obtener los datos de la request.
        parser.add_argument("Sistema", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Id")
        parser.add_argument("Status", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #Obtenemos los datos de la request.
        if data['Sistema'] == 'Zendesk':
            with switch_db(ModelTicketAudit, session["dbMongoEngine"]):
                my_model = ModelTicketAudit.objects(Id=data['Id']).first() # <--- Buscara en los documentos el id y el sistema enviado por el front end.
                my_model.Status = data['Status']
                # creds = json.loads(session["user"]["ticketSystemAttr"])                          
                # zenpy_client = Zenpy(**creds)
                ticket = zenpy_client.tickets(id=my_model.Id)
                ticket.status = my_model.Status
                zenpy_client.tickets.update(ticket) # <--- Con los parametros de ID y Comentario se actualizara el ticket.
                my_model.save()
            return jsonify(my_model.to_json())
        elif data['Sistema'] == 'Freshdesk':
            with switch_db(ModelTicketAudit, session["dbMongoEngine"]):
                my_model = ModelTicketAudit.objects(Id=data['Id']).first()
                my_model.Status = data['Status']
                if data['Status'] == 'open':
                    verify = 2
                elif data['Status'] == 'pending':
                    verify = 3
                elif data['Status'] == 'solved':
                    verify = 4
                # creds = json.loads(session["user"]["ticketSystemAttr"])  
                # credfresh = API(**creds) 
                credfresh.tickets.update_ticket(ticket_id=my_model.Id, status=verify)
                my_model.save()
            return jsonify(my_model.to_json())

class returnSystemTicket(Resource):
    
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):
        parser = reqparse.RequestParser() #Creamos un objeto para obtener los datos de la request.
        parser.add_argument("Requester", type=str, required=False, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Sistema", type=str, required=True, help="Mensaje que devolvera en caso de parametro mal ingresado")
        parser.add_argument("Status", type=str, required=False, help="Mensaje que devolvera en caso de parametro mal ingresado")
        data = parser.parse_args() #Obtenemos los datos de la request.
        if data['Sistema'] == 'Zendesk':
            # creds = json.loads(session["user"]["ticketSystemAttr"])                          
            # zenpy_client = Zenpy(**creds)
            list_ticket = []
            if data['Requester'] == None :
                if data['Status'] != None:
                    for ticket in zenpy_client.search(type='ticket', status=data['Status']):
                        list_ticket.append(ticket.to_json())
                else:
                    for ticket in zenpy_client.search(type='ticket'):
                        list_ticket.append(ticket.to_json())
            elif data['Requester'] != None :
                if  data['Status'] == None :
                    for ticket in zenpy_client.search(type='ticket', requester=data['Requester']):
                        list_ticket.append(ticket.to_json())
                else:
                    for ticket in zenpy_client.search(type='ticket', status=data['Status'], requester=data['Requester']):
                        list_ticket.append(ticket.to_json())
            return jsonify(list_ticket)
        elif data['Sistema'] == 'Freshdesk':
            # creds = json.loads(session["user"]["ticketSystemAttr"])  
            # credfresh = API(**creds) 
            if data['Status'] == 'open':
                ticket = credfresh.tickets.list_tickets(filter_name='new_and_my_open')
                list_ticket = [str(i) for i in ticket]
            elif data['Status'] == 'solved':
                ticket = credfresh.tickets.list_tickets(filter_name='watching')
                list_ticket = [str(i) for i in ticket]
            return json.dumps(list_ticket)
            
             
            



    #documentacion sobre requestParser https://flask-restful.readthedocs.io/en/latest/reqparse.html
    #documentacion sobre decoradores https://github.com/alloxentric/KeycloakAuth
    #docuemntacion sobre flask https://flask.palletsprojects.com/en/2.0.x/
    #documentacion sobre flask restful https://flask-restful.readthedocs.io/en/latest/
