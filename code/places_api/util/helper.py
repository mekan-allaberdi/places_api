import requests, json

def get_response(url, params):
    """
    Gets response of url.

    Args:
        url (string) : ulr of request
        params (dict) : params of dict
    Returns:
        json result.
    """
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data

def json_status_ok(data_json, status_attr):
    """
    Check status of response json.

    Args:
        data_json (json) : json data
    Returns:
        status OK or NOT
    """
    status = data_json[status_attr]
    return status == 'OK'


def get_tree_data(data, attributes):
    """
    Gets multiple inner tree data of json.

    Args:
        data_json (json) : json data
        attributes (list) : list of attributes
    Returns:
        element of json
    """
    for attr in attributes:
        if type(attr) is int:
            if attr < len(data):
                data = data[attr]
            else:
                return None
        elif type(attr) is list:
            datas = {}
            for key in attr:
                if key in data:
                    datas[key] = data[key]
            return datas
        elif attr in data:
            data = data[attr]
        else:
            return None
    return data

def parse_attributes(data, attributes):
    """
    Parses json attributes and sends result.

    Args:
        data_json (json) : json data
        attributes (2D list) : list of attributes
    Returns:
        elements of json
    """
    result = {}
    for key, val in attributes.items():
        if type(val) is list:
            attr_val = get_tree_data(data, val)
        else:
            attr_val = data.get(val, None)
        if attr_val is not None:
            result[key] = attr_val
    return result
