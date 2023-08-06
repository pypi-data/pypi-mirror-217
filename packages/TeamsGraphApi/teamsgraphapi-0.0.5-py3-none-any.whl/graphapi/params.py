from urllib.parse import urlencode


def get_params(param):
    """
    used to get the params for only message api
    """
    query_string = urlencode(param, doseq=True)

    url = "?" + query_string

    return url


