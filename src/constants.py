from enum import Enum

VERSION_1 = "/v1"
API = "/api"
API_URL_V1 = f"{API}{VERSION_1}"

class HttpClientCommonErrorsLiteral(Enum):
    SOMETHING_WENT_WRONG = "Something went wrong, please try again later"
