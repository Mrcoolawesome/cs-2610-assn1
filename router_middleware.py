from http_parser import response_parser
from endpoints import home, about, expierence, projects, info

# logs the attributes of both http-requests and http-responses to the console
def logging_middleware_factory(next):  
    def middleware(http_object):  
        # print request 
        print(f"Request recieved: {http_object.method} {http_object.uri}")
        #call next middleware
        res = next(http_object)
        # print response, notice the request is still in scope!
        print(f"{http_object.uri} {res.code} {res.reason}") 
        return res
    
    return middleware
    
# Static files - this simply reads .js or .css files, then adds them to the http response. it'll add the text onto the response objects '.text' attribute
def static_middleware_factory(next):  
    def middleware(http_object):  
        if "." in http_object.uri:
            filename = f"static{http_object.uri}"
            response = response_parser(http_object, filename)
            return response
        
        res = next(http_object) 
        return res
      
    return middleware 

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
# ARE WE ALLOWED TO ADD A MIDDLEWARE TO THIS LIST MORE THAN ONCE, BECAUSE THAT'S WHAT MAKES THE LOGGER WORK?
#   SINCE ANYWHERE PAST THE ROUTER OR STATIC FUNCTIONS A RESPONSE IS PASSED, IT CAN ONLY LOG RESPONSES PASSED THESE FUNCTIONS
#   AND IT CAN ONLY LOG REQUESTS BEFORE THESE FUNCTIONS
middleware_factory_list = [logging_middleware_factory, router_middleware_factory, static_middleware_factory]

def compose(end_result_function, middleware_factory_list):
    for middleware in reversed(middleware_factory_list):
        end_result_function = middleware(end_result_function)
    return end_result_function

def middleware_router(http_request):
    return compose(static_middleware_factory, middleware_factory_list)(http_request)
      
# router will redirect the object to the endpoints if it's an html, or just skip to the middleware if it's asking for a .js or .css file