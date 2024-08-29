from http_parser import response_parser

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