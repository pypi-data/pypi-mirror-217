import uuid
import asyncio
import json
import warnings
import re

import httpx

from MiPC.exceptions import MisskeyMiAuthFailedException

class MiAuth:

    def __init__(
        self, 
        server="misskey.io", 
        name="MiPC Application"
    ):
        self.__pattern = "http?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        self.__pattern_ws = "^ws:\/\/.*"
        if re.match(self.__pattern_ws, server):
            raise TypeError("Websocket procotr is not available within the Misskey class.")
        if re.match(self.__pattern, server):
            self.server = server
        else:
            self.server = "https://" + server
        self.name = name
    
    def generate(
            self, 
            permission=["read:account", "write:account", "read:blocks", "write:blocks", "read:drive", "write:drive", "read:favorites", "write:favorites", "read:following", "write:following", "read:messaging", "write:messaging", "read:mutes", "write:mutes", "write:notes", "read:notifications", "write:notifications", "write:reactions", "write:votes", "read:pages", "write:pages", "write:page-likes", "read:page-likes", "write:gallery-likes", "read:gallery-likes"]
    ):
        self.session_id = uuid.uuid4()
        url = f"{self.server}/miauth/{self.session_id}?name={self.name}&permission={','.join(permission)}"
        return url
    
    def token(
            self
    ):
        url = f"{self.server}/api/miauth/{self.session_id}/check"
        response = httpx.post(url)
        response_json = response.json()
        if response_json["ok"]:
            return response_json["token"]
        else:
            raise MisskeyMiAuthFailedException(response_json)