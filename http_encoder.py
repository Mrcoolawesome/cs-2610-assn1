# this turns a http_response object into a string and then into bytes, which it then returns to the server
def encoder(response_object):
    # make sure everything is seperated by spaces in the first line
    response = f"{response_object.version} " \
            + f"{response_object.code} " \
            + f"{response_object.reason}\n"
    
    # convert each header 
    headers = ""
    for header, value in response_object.headers.items():
        headers += header + ": " + value + "\n"
        
    # add the headers and body onto the http response, making sure to leave a newline between the two
    response += headers + "\n" + response_object.text
    
    # convert the response into bytes and return it to the server
    encoded_response = bytes(response, "UTF-8")
    return encoded_response