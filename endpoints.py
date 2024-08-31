from http_parser import response_parser

# each endpoint returns a response object based on the request and their corresponding file
def home(http_request):
    return response_parser(http_request, "templates/index.html")

def about(http_request):
    return response_parser(http_request, "templates/about.html")
    
def expierence(http_request):
    return response_parser(http_request, "templates/expierence.html")
    
def projects(http_request):
    return response_parser(http_request, "templates/projects.html")

def info(http_request):
    return response_parser(http_request, "templates/about.html", 301)