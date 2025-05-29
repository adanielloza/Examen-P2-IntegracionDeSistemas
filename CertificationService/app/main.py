from spyne import Application, rpc, ServiceBase, Integer, Unicode, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class CertificationService(ServiceBase):
    @rpc(Integer, Unicode, _returns=Boolean,
         _in_variable_names={'studentId': 'studentId', 'type': 'type'})
    def RegisterCert(ctx, studentId, type):
        """
        Mock implementation: always returns True == success.
        """
        # you could add logging here, or simulate failures if you like
        return True

# Create a Spyne application
soap_app = Application(
    [CertificationService],
    tns="http://example.com/certservice",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(soap_app)

if __name__ == "__main__":
    # Bind to 0.0.0.0:8006
    server = make_server("0.0.0.0", 8006, wsgi_app)
    print("Starting SOAP CertificationService on http://0.0.0.0:8006")
    server.serve_forever()
