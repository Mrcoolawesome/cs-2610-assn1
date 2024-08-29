from request_response import Request, Response
from http_encoder import encoder
from endpoints import home, about, expierence, projects, info

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
            filename = f"static{http_object.uri}"
            return encoder(http_object, filename)
        
        res = next(http_object) 
        return res # don't forget this step!  
      
    return middleware # don't forget this step!

def router_middleware_factory(next): # do we treat the router as middleware?!!!!!!!!!!!!!!!!!!!!!!!!!
    def router(http_object):
        if "." not in http_object.uri:
            # you return this to the server that transmits it
            if http_object.uri == "/":
                return home(http_object)
            elif http_object.uri == "/about":
                return about(http_object)
            elif http_object.uri == "/expierence":
                return expierence(http_object)
            elif http_object.uri == "/projects":
                return projects(http_object)
            elif http_object.uri == "/info":
                return info(http_object)
        res = next(http_object)
        return res
    
    return router
        
# the order of these do matter, i've ordered it from 1'st used to last
middleware_factory_list = [logging_middleware_factory, router_middleware_factory, static_middleware_factory]

def compose(end_result_function, middleware_factory_list):
    for middleware in reversed(middleware_factory_list):
        end_result_function = middleware(end_result_function)
    return end_result_function

def middleware_router(http_request):
    return compose(static_middleware_factory, middleware_factory_list)(http_request)
      
# router will redirect the object to the endpoints if it's an html, or just skip to the middleware if it's asking for a .js or .css file