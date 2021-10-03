from enum import Enum, auto


class ClientResponse(Enum):
    SUCCESS = auto()
    CREATED = auto()
    FAILED = auto()
    INVALID = auto()
    EXISTS = auto()
    NOTFOUND = auto()
    INTERNALERROR = auto()


class UserAgents(Enum):
    """Holds different User Agents for scraping modules."""
