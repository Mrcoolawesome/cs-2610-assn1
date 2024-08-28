# http encoder - will create valid http responses containing the content in the .js, .css, or .html files that are requested
# then it sends those files back to the client
from server import send_bytes
from request_response import Response
from datetime import time, date

def encoder(http_request):
    file_type = http_request.uri.split(".")[1]
    if file_type == "js" or file_type == "css":
        filename = "static" + http_request.uri
    elif file_type == "html":
        filename = "template" + http_request.uri
    
    # this will handle if the file isn't found
    response_object = create_response(filename, http_request.version)
    
    # make sure everything is seperated by spaces in the first line
    response = response_object.version + " " \
            + response_object.code + " " \
            + response_object.reason + "\n"
    
    # get the headers 
    headers = ""
    for header, value in response_object.headers.items():
        headers += header + ": " + value + "\n"
        
    response += headers + response_object.text
    encoded_response = bytes(response, "UTF-8")
    send_bytes(encoded_response)
            

def create_response(filename, version):
    response = Response("","","","","")
    http_text = ""
    http_length = 0
    try:
        file = open(filename)
        for line in file:
            http_text += line
            http_length += len(line)
        file.close()
        response.text = http_text
    except FileNotFoundError:
        # have the response be a 404 file not found
        response.code = 404
        response.headers = {"Server" : "DevinIsCool",
                            "Date" : f"{time} | {date}",
                            "Connection" : "close",
                            "Cache-Control" : "max-age-2"
                            }
        response.reason = "Not Found"
        response.version = version   
        return response     
    # account for other errors
    
    # if we've made it here that means everything's all good
    # .js, .css, and .html files all start with the 'text/' string for the 'content-type' header
    response.code = 200
    response.headers = {"Server" : "DevinIsCool",
                            "Date" : f"{time} | {date}",
                            "Connection" : "close",
                            "Cache-Control" : "max-age-2",
                            "Content-Length" : f"{http_length}"
                            }
    response.reason = "OK"
    response.version = version
    response.text = http_text
        
    return response    
        
    