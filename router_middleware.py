from request_response import Request, Response

# logs the attributes of both http-requests and http-responses to the console
def logging_middleware_factory(next):  
    def middlware(http_object):  
        if isinstance(http_object, Request):
            print(f"Request recieved: {http_object.method} {http_object.uri}")
        elif isinstance(http_object, Response):
            print(f"{http_object.uri} {http_object.code} {http_object.reason}")
        else:
            raise TypeError("The http-object supplied is not an expected type. Expected Request or Response.")
        
        res = next(http_object) # call the next middleware in the chain  
        return res
    
    return middlware
    
# Static files 
def middleware_factory(next):  
    def middlware(my_input):  
        # Do something with my_input (optional)  
        res = next(my_input) # call the next middleware in the chain  
        # do something with res (optional)  
        return res # don't forget this step!  
      
    return middlware # don't forget this step!
      