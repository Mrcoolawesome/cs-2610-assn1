# this turns a http_response object into a string and then into bytes, which it then returns to the server
def encoder(response_object):
    # make sure everything is seperated by spaces in the first line
    response = f"{response_object.version} " \
            + f"{response_object.code} " \
            + f"{response_object.reason}\n"
    
    # get the headers 
    headers = ""
    for header, value in response_object.headers.items():
        headers += header + ": " + value + "\n"
        
    response += headers + "\n" + response_object.text
    encoded_response = bytes(response, "UTF-8")
    return encoded_response