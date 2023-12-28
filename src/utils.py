from fastapi.routing import APIRoute


def generate_endpoint_name(route: APIRoute):
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name
