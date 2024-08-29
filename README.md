# Dataflow
1. The data is first recieved by server.py
2. Then that data is converted by http_parser.py into a Request object
3. The Request object is returned to the server, that gives that object to the router & middleware (router_middleware.py)
4. The object goes through the router/middleware.
    - The first thing the middleware does is log the Request using the `logging_middleware_factory` function, then pass the request onto the rest of the middleware
    - If the Request is asking for an html file, then the router gives the object to the correct endpoint
        - Then that endpoint simply has the response_parser in `http_parser.py` read the information from the correct file, and then return a Response object
        - This Response object then gets returned to the router, which passes on the Response down the middleware chain
    - If the Request is asking for a `.js` or `.css` file, then the Request object is passed onto the rest of the middleware, where it'll be taken by the `static_middleware`
        - This middleware will do what the enpoints do, but for `.js` and `.css` files, then passes on the Response object to the rest of the middleware.
    - The Response object is then logged using the same `logging_middleware_factory` function as before.
    - Finally the Response object is given to the last middlware that encodes the Response object into a valid http-response code, then returns it as bytes to `server.py`, where the bytes are sent back to the client.