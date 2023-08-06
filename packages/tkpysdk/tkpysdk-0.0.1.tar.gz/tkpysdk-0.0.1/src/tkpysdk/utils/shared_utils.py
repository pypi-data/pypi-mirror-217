# Author: Sirui Ray Li
# Created: 7/6/23
# Version: 1.0
# Description:
from requests import Response


def process_response(res: Response):
    if res.status_code == 200:
        return res.json()
    else:
        return res.text
