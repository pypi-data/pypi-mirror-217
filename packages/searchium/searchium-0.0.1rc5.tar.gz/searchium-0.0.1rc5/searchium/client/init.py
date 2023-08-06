class Config(object):
    allocation_id: str = None
    url_searchium: str = None
    port: int = None
    link: str = None
    headers: str = None

    def __init__(self, allocation_id: str, url_searchium: str, cloud: bool = True, port: int = 7760, apiv: str = 'v1.0') -> None:
        if Config.allocation_id is None and Config.url_searchium is None:
            Config.allocation_id = allocation_id
            Config.url_searchium = url_searchium
            Config.port = port
            Config.link = f"{Config.url_searchium}/v1.0" if cloud else f"{Config.url_searchium}:{Config.port}/{apiv}"
            Config.headers = {'Content-Type': 'application/json', 'allocationToken': f'{Config.allocation_id}'}


def init(allocation: str, url: str, cloud: bool = True, port: int = 7760, apiv: str = 'v1.0') -> None:
    """
    Init configuration client of FVS Searchium
    All these params as allocation & url you can receive
     on our cloud platform searchium.ai
    :param apiv:
    :param cloud:
    :param allocation: str = instance id uuid
    :param port: as default 7760
    :param url: str
    :return: None
    """
    Config(allocation, url, cloud, port, apiv)
