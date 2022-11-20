#from email.policy import default
#from msilib.schema import CheckBox
#from xmlrpc.client import boolean
from email.policy import default
from mongoengine import Document, DynamicDocument
from mongoengine import StringField, BooleanField, IntField, FileField

class ModelTicketAudit(Document):

    sistema = {
        'Zendesk':'Zendesk',
        'Freshdesk':'Freshdesk'
                                # <--- Aqui se debe ingresar el nuevo sistema
    }
    Id = IntField()
    Sistema = StringField(max_length=128, choices=sistema.keys(), required=True)
    Requester = StringField(max_length=128, required=True)
    Email = StringField(max_length=128, required=True)
    Subject = StringField(max_length=150, required=True)
    Description = StringField(max_length=1000, required=True)
    Comment1 = StringField(max_length=1000, required=False)
    Status = StringField(max_length=1000, required=False)
    Archivo = FileField(required=False)
