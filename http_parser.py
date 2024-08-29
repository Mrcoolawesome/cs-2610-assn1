# we need to parse the http request given to us, and turn it into the Request object and return that
from request_response import Request, Response

# takes the raw data and turns it into a request object
def request_parser(data):
    request = Request("","","","","")
    raw_http = str(data, "UTF-8")
    http_split = raw_http.splitlines() # list whose first two items are important
    first_line_info = http_split[0].split() # this contains the verb/method, uri, and version
    if len(first_line_info) == 3:
        request.method = first_line_info[0]
        request.uri = first_line_info[1]
        request.version = first_line_info[2]
        request.text = raw_http
        request.headers = header_parser(http_split)
    else: 
        raise IndexError("Either all or one of the following are missing or formatted wrong: method | uri | version")
        # then somehow throw an http error
    
    return request

# takes a list of http request/response lines, then converts the headers and values into key-value pairs in a dictionary
def header_parser(http_text):
    header_value_dict = {}
    for line in http_text:
        if ":" in line:
            key_value = line.split(":")
            if len(key_value) == 2:
                header_value_dict[key_value[0].strip()] = key_value[1].strip()
            else: 
                pass
    return header_value_dict
            