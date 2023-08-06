import io
import os
import uuid
from typing import (
    Optional,
    Union,
    List,
    Tuple,
    Set,
    Any,
    IO as IOTypes,
)
import zlib
import warnings
import json
import sys
import traceback
import re

import mimetypes
import httpx
import websockets
import aiofiles
from colorama import Fore, Back, Style
from websockets import connect, exceptions
import orjson

from MiPC.exceptions import MisskeyMiAuthFailedException, MisskeyAPIException
import MiPC

Arry = list

class user:
    pass

class Misskey:
    
    def __init__(
        self, server, token=None):
        self.__pattern = "http?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        self.__pattern_ws = "^ws:\/\/.*"
        if re.match(self.__pattern_ws, server):
            raise TypeError("Websocket procotr is not available within the Misskey class.")
        if re.match(self.__pattern, server):
            self.__server = server
        else:
            self.__server = "https://" + server
        self.__token = token
        self.http = MiPC.sync_mihttp(server)

    def meta(
        self):
        class metadata:
            pass
        params = {
            "i" : self.__token,
        }
        headers = {
            "Content-Type": "application/json"
        }
        with httpx.Client() as client:
            r = client.post(
                url=f'{self.__server}/api/meta', 
                json=params,
                headers=headers
            )
            rj = json.loads(r.text)
            meta = metadata
            try:
                meta.maintainer = [rj["maintainerName"], rj["maintainerEmail"]]
                meta.version = rj["version"]
                meta.name = rj["name"]
                meta.url = rj["uri"]
                meta.description = rj["description"]
                meta.lang = rj["langs"]
                meta.tos = rj["tosUrl"]
                meta.full = json.dumps(rj, ensure_ascii=False, indent=4)
                return meta
            except Exception as e:
                raise MisskeyAPIException(f"Failed to retrieve metadata. status code: {r.status_code}\n\n{traceback.format_exc()}")

    def upload(
        self,
        file
    ):
        params = {
            'i' : self.__token,
        }
        with httpx.Client() as client:
            r = client.post(
                url=f'{self.__server}/api/drive/files/create', 
                data=params,
                files={"file" : file}
            )
            return r

    def delete(
        self,
        file_id: str
    ):
        return self.http.request('drive/files/delete', data={
            "fileId": file_id
        })

    def update(
        self, 
        dct: dict
    ):
        dct["i"] = self.__token
        return self.http.request('i/update', data=dct)

    def send(
        self, 
        text, 
        visibility="public", 
        visibleUserIds: list=None, 
        replyid=None, 
        fileid=None, 
        channelId=None, 
        localOnly=False
    ):
        url = f"{self.__server}/api/notes/create"
        if replyid is not None:
            if fileid is not None:
                params = {
                    "i" : self.__token,
                    "replyId": replyid,
                    "fileIds": fileid,
                    "visibility": visibility,
                    "visibleUserIds": visibleUserIds,
                    "channelId": channelId,
                    "localOnly": localOnly,
                    "text": text
                }
                head = {
                    "Content-Type": "application/json"
                }
                with httpx.Client() as client:
                    r = client.post(
                        url=url, 
                        json=params,
                        headers=head
                    )
                    return r.json()
            else:
                if visibleUserIds is None:
                    params = {
                        "i" : self.__token,
                        "replyId": replyid,
                        "visibility": visibility,
                        "channelId": channelId,
                        "localOnly": localOnly,
                        "text": text
                    }
                    head = {
                        "Content-Type": "application/json"
                    }
                    with httpx.Client() as client:
                        r = client.post(
                            url=url, 
                            json=params,
                            headers=head
                        )
                        return r.json()
                else:
                    params = {
                        "i" : self.__token,
                        "replyId": replyid,
                        "visibility": visibility,
                        "visibleUserIds": visibleUserIds,
                        "channelId": channelId,
                        "localOnly": localOnly,
                        "text": text
                    }
                    head = {
                        "Content-Type": "application/json"
                    }
                    with httpx.Client() as client:
                        r = client.post(
                            url=url, 
                            json=params,
                            headers=head
                        )
                        return r.json()
        else:
            params = {
                "i" : self.__token,
                "text": text
            }
            head = {
                "Content-Type": "application/json"
            }
            with httpx.Client() as client:
                r = client.post(
                    url=url, 
                    json=params,
                    headers=head
                )
                return r.json()

    def renote(self, rid: str, quote: str=None, visibility="public", visibleUserIds: list=None, channelId=None, localOnly=False):
        url = f"{self.__server}/api/notes/create"
        if quote is None:
            params = {
                "i" : self.__token,
                "renoteId": rid,
                "localOnly": localOnly,
                "channelId": channelId,
            }
            head = {
                "Content-Type": "application/json"
            }
            with httpx.Client() as client:
                r = client.post(
                    url=url, 
                    json=params,
                    headers=head
                )
                return r.json()
        else:
            if visibleUserIds is None:
                params = {
                    "i" : self.__token,
                    "renoteId": rid,
                    "visibility": visibility,
                    "localOnly": localOnly,
                    "channelId": channelId,
                    "text": quote
                }
                head = {
                    "Content-Type": "application/json"
                }
                with httpx.Client() as client:
                    r = client.post(
                        url=url, 
                        json=params,
                        headers=head
                    )
                    return r.json()
            else:
                params = {
                    "i" : self.__token,
                    "renoteId": rid,
                    "visibility": visibility,
                    "visibleUserIds": visibleUserIds,
                    "localOnly": localOnly,
                    "channelId": channelId,
                    "text": quote
                }
                head = {
                    "Content-Type": "application/json"
                }
                with httpx.Client() as client:
                    r = client.post(
                        url=url, 
                        json=params,
                        headers=head
                    )
                    return r.json()

    def app_create(
        self, 
        name, 
        description, 
        permission=["read:account", "write:account", "read:blocks", "write:blocks", "read:drive", "write:drive", "read:favorites", "write:favorites", "read:following", "write:following", "read:messaging", "write:messaging", "read:mutes", "write:mutes", "write:notes", "read:notifications", "write:notifications", "write:reactions", "write:votes", "read:pages", "write:pages", "write:page-likes", "read:page-likes", "write:gallery-likes", "read:gallery-likes"],
        callback=None
    ):
        if callback is None:
            r = self.http.request(
                "app/create", 
                {"name": name, "description": description, "permission": permission}
            )
        else:
            r = self.http.request(
                "app/create", 
                {"name": name, "description": description, "permission": permission, "callbackUrl": callback}
            )

        return r