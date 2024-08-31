from http_parser import response_parser
from endpoints import home, about, expierence, projects, info
from request_response import Response

# the router decides what endpoint to call on based on a request object, and handles http errors
def router_middleware_factory(next):
    def router(http_object):
        # if there's not a '.' present in the uri, the request is looking for a new page
        if "." not in http_object.uri:
            # dictionary of endpoint names and corresponding function
            endpoints = {
                "/" : home,
                "/about" : about,
                "/expierence" : expierence,
                "/projects" : projects,
                "/info" : info
            }
            
            # iterate through the dictionary, and use the endpoint that corresponds to the uri
            for key, value in endpoints.items():
                if key == http_object.uri:
                    # returns an http_response object
                    return value(http_object)
        
        res = next(http_object)
        # if anything besides a response object was returned then the page was not found. the response_parser will return a 404 error
        if res != isinstance(res, Response):
            filename = f"static{http_object.uri}"
            response = response_parser(http_object, filename)
            return response
    
        return res
    
    return router

# logs the attributes of both http-requests and http-responses to the console
def logging_middleware_factory(next):  
    def middleware(http_object):  
        # print request 
        print(f"Request recieved: {http_object.method} {http_object.uri}")
        
        # call next middleware
        res = next(http_object)
        
        # print response
        print(f"{http_object.uri} {res.code} {res.reason}") 
        
        # return the result of the last middleware used
        return res
    
    return middleware
    
# Static files - this simply reads .js or .css files, then adds them to the http response
def static_middleware_factory(next):  
    def middleware(http_object):  
        # we know if it's looking for a specific file if the uri contains a '.' in it
        if "." in http_object.uri:
            filename = f"static{http_object.uri}"
            
            # create a response object based off of the request and filename
            response = response_parser(http_object, filename)
            return response
        
        res = next(http_object) 
        return res
      
    return middleware 
        
# the order of these do matter, i've ordered it from 1'st used to last
middleware_factory_list = [logging_middleware_factory, router_middleware_factory, static_middleware_factory]

# this composes all the middleware (including the router) into one callable function
def compose(end_result_function, middleware_factory_list):
    for middleware in reversed(middleware_factory_list):
        end_result_function = middleware(end_result_function)
    return end_result_function

# composes all the middleware, taking in only an http_request object
def middleware_router(http_request):
    return compose(static_middleware_factory, middleware_factory_list)(http_request)