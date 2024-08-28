from request_response import Request, Response
from http_encoder import encoder
# logs the attributes of both http-requests and http-responses to the console
def logging_middleware_factory(next):  
    def middleware(http_object):  
        if isinstance(http_object, Request):
            print(f"Request recieved: {http_object.method} {http_object.uri}")
        elif isinstance(http_object, Response):
            print(f"{http_object.uri} {http_object.code} {http_object.reason}")
        else:
            raise TypeError("The http-object supplied is not an expected type. Expected Request or Response.")
        
        res = next(http_object) # call the next middleware in the chain  
        return res
    
    return middleware
    
# Static files - this simply reads .js or .css files, then adds them to the http response. it'll add the text onto the response objects '.text' attribute
def static_middleware_factory(next):  
    def middleware(http_object):  
        if "." in http_object.uri:
            encoder(http_object)
        
        res = next(http_object) 
        return res # don't forget this step!  
      
    return middleware # don't forget this step!

def router(http_object):
    if "." not in http_object.uri:
        # you return this to the server that transmits it
        if http_object.uri == "/":
            # read the templates/index.html file
            pass
        elif http_object.uri == "/about":
            # read the templates/about.html file
            pass
        elif http_object.uri == "/expierence":
            # read the templates/expierence.html file
            pass
        elif http_object.uri == "/projects":
            # read the templates/projects.html file
            pass
        elif http_object.uri == "/info":
            # read the templates/info.html file
            pass
        pass
      
      
# router will redirect the object to the endpoints if it's an html, or just skip to the middleware if it's asking for a .js or .css file