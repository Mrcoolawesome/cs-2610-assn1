from request_response import Request, Response
from datetime import datetime

# takes the raw data and turns it into a request object
def request_decoder(data):
    request = Request("","","","","")
    
    # convert data from bytes to a string
    raw_http = str(data, "UTF-8")

    # splits each line of the raw-http string and puts them into a list
    http_split = raw_http.splitlines()
    
    # this list contains the verb/method, uri, and version
    first_line_info = http_split[0].split() 
    
    # assign the info from the first line onto each attribute of the request object
    request.method = first_line_info[0]
    request.uri = first_line_info[1]
    request.version = first_line_info[2]
    request.text = raw_http
    request.headers = header_parser(http_split)
    
    return request

# takes a list of http headers, then converts the headers and values into key-value pairs in a dictionary
def header_parser(http_text):
    header_value_dict = {}
    for line in http_text:
        # we know if there's a header on a line if there's a ':' on the line
        if ":" in line:
            # list that contains the name and the value of a header
            key_value = line.split(":")
            
            # make a new key and value for the dictionary, making sure to remove any unnecessary white space
            header_value_dict[key_value[0].strip()] = key_value[1].strip()
            
    return header_value_dict

# response parser - will create valid http response objects containing the content in the .js, .css, or .html files that are given to it
def response_parser(http_request, filename, code=200):
    # create_response will handle if the file isn't found
    response_object = create_response(filename, http_request, code)
    return response_object

# responsible for creating a valid http response object. creates a 404 or 301 code http response if required
def create_response(filename, http_request, code):
    # get the current time
    now = datetime.now()
    current_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # create the response object and initalize its attributes
    response = Response("","","","","")
    http_text = ""
    http_length = 0
    
    # get the name of the file type, it should be the last element of this list
    split_filename = filename.split(".")
    file_type = split_filename[len(split_filename) - 1]
    if file_type == "js":
        file_type = "javascript"
    
    try:
        file = open(filename)
        # simply add each line onto the http response's body
        for line in file:
            http_text += line
            http_length += len(line)
        file.close()
        
        # add the text to the response object
        response.text = http_text
    except FileNotFoundError:
        # have the response be a 404 file not found, with a basic header to explain what happened
        response.code = 404
        response.headers = {
            "Server" : "DevinIsCool",
            "Date" : f"{current_time}",
            "Connection" : "close",
            "Cache-Control" : "max-age-2",
            "Content-Type" : f"text/html"
            }
        response.reason = "Not Found"
        response.version = http_request.version
        response.text = "<h1> Could not find the page you're looking for! </h1>"
        return response     
    
    # if there's a redirect requested
    if code == 301:
        response.code = code
        response.headers = {
            "Server" : "DevinIsCool",
            "Date" : f"{current_time}",
            "Connection" : "close",
            "Cache-Control" : "max-age-2",
            "Location" : f"http://localhost:8000/about"}
        response.reason = "Moved Permenantly"
        response.version = http_request.version
    else: # if we've made it here that means everything's all good and the response code is 200!
        response.code = code
        # .js, .css, and .html files all start with the 'text/' string for the 'content-type' header value
        response.headers = {
            "Server" : "DevinIsCool",
            "Date" : f"{current_time}",
            "Connection" : "close",
            "Cache-Control" : "max-age-2",
            "Content-Length" : f"{http_length}",
            "Content-Type" : f"text/{file_type}"
            }
        response.reason = "OK"
        response.version = http_request.version
        response.text = http_text
    return response    
        