from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import json

# species to credentials mapping
species_credentials = {
    "Time Lord": "Rassilon",
    "Cyberman": "John Lumic",
    "Dalek": "Davros",
    "Judoon": "Shadow Proclamation Convention 15 Enforcer",
    "Human": "Leonardo da Vinci",
    "Ood": "Klineman Halpen",
    "Silence": "Tasha Lem",
    "Slitheen": "Coca-Cola salesman",
    "Sontaran": "General Staal",
    "Weeping Angel": "The Division Representative",
    "Zygon": "Broton",
}


def application(environ, start_response):
    # extract species from GET parameters
    query = parse_qs(environ['QUERY_STRING'])
    # get species or empty string if not present
    species = query.get('species', [''])[0]

    # determine the response
    if species in species_credentials:
        status = '200 OK'
        credentials = species_credentials[species]
    else:
        status = '404 NOT FOUND'
        credentials = "Unknown"

    # create response
    response_body = json.dumps({"credentials": credentials}).encode('utf-8')
    response_headers = [('Content-Type', 'application/json'),
                        ('Content-Encoding', 'utf-8'),
                        ('Content-Length', str(len(response_body)))]

    # start response
    start_response(status, response_headers)

    # return body
    return [response_body]


# create server
port = 8888
httpd = make_server('127.0.0.1', port, application)
print(f"Serving on port {port}...")

# start server
httpd.serve_forever()
