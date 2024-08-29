from request_response import Request, Response
from http_encoder import encoder
from endpoints import home, about, expierence, projects, info

# logs the attributes of both http-requests and http-responses to the console
def logging_middleware_factory(next):  
    def middleware(http_object):  
        if isinstance(http_object, Request):
            print(f"Request recieved: {http_object.method} {http_object.uri}")
        elif isinstance(http_object, Response):
            print(f"{http_object.code} {http_object.reason}")
        else:
            raise TypeError("The http-object supplied is not an expected type. Expected Request or Response.")
        
        res = next(http_object) # call the next middleware in the chain  
        return res
    
    return middleware
    
# Static files - this simply reads .js or .css files, then adds them to the http response. it'll add the text onto the response objects '.text' attribute
def static_middleware_factory(next):  
    def middleware(http_object):  
        if isinstance(http_object, Request) and "." in http_object.uri:
            filename = f"static{http_object.uri}"
            response = encoder(http_object, filename)
            res = next(response)
            return res
        
        res = next(http_object) 
        return res
      
    return middleware 

# this turns a http_response object into a string and then into bytes, which it then returns to the server
def encoding_middleware_factory(next):
    def middleware(http_object):
        if isinstance(http_object, Response):
            # make sure everything is seperated by spaces in the first line
            response = f"{http_object.version} " \
                    + f"{http_object.code} " \
                    + f"{http_object.reason}\n"
            
            # get the headers 
            headers = ""
            for header, value in http_object.headers.items():
                headers += header + ": " + value + "\n"
                
            response += headers + "\n" + http_object.text
            encoded_response = bytes(response, "UTF-8")
            return encoded_response
        res = next(http_object) 
        return res # don't forget this step!  
    return middleware

def router_middleware_factory(next): # do we treat the router as middleware?!!!!!!!!!!!!!!!!!!!!!!!!!
    def router(http_object):
        if isinstance(http_object, Request) and "." not in http_object.uri:
            # you return this to the server that transmits it
            response = Response("","","","","")
            if http_object.uri == "/":
                response = home(http_object)
            elif http_object.uri == "/about":
                response = about(http_object)
            elif http_object.uri == "/expierence":
                response = expierence(http_object)
            elif http_object.uri == "/projects":
                response = projects(http_object)
            elif http_object.uri == "/info":
                response = info(http_object)
            res = next(response)
            return res
        
        res = next(http_object)
        return res
    
    return router
        
# the order of these do matter, i've ordered it from 1'st used to last
# ARE WE ALLOWED TO ADD A MIDDLEWARE TO THIS LIST MORE THAN ONCE, BECAUSE THAT'S WHAT MAKES THE LOGGER WORK?
#   SINCE ANYWHERE PAST THE ROUTER OR STATIC FUNCTIONS A RESPONSE IS PASSED, IT CAN ONLY LOG RESPONSES PASSED THESE FUNCTIONS
#   AND IT CAN ONLY LOG REQUESTS BEFORE THESE FUNCTIONS
middleware_factory_list = [logging_middleware_factory, router_middleware_factory, static_middleware_factory, logging_middleware_factory, encoding_middleware_factory]

def compose(end_result_function, middleware_factory_list):
    for middleware in reversed(middleware_factory_list):
        end_result_function = middleware(end_result_function)
    return end_result_function

def middleware_router(http_request):
    return compose(encoding_middleware_factory, middleware_factory_list)(http_request)
      
# router will redirect the object to the endpoints if it's an html, or just skip to the middleware if it's asking for a .js or .css file