from enum import Enum


class HTTPMethod(str, Enum):
    """HTTP methods as defined in RFC 7231 section 4.3."""

    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
