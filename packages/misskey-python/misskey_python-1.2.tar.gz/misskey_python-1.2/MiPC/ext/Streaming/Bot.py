import json
import re
import asyncio

import httpx
import websockets

from MiPC import Misskey

class Bot():

    class context:
        
        class nt:
            id = ""
        
        class auth:
            class hst:
                name = ""
                software = ""
                softwareversion = ""
                icon = ""
                favicon = ""
                color = ""
            id = ""
            name = ""
            username = ""
            host = hst()
        
        class rid:
            id = ""
            
        class rnid:
            id = ""
        
        note = nt()
        author = auth()
        reply = rid()
        renote = rnid()

    def __init__(self, server, token):
        self.__token = token
        self.__pattern = "^ws:\/\/.*"
        self.__pattern_2 = "http?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        if re.match(self.__pattern, server):
            self.__server = server
        else:
            self.__server = "wss://" + server
        if re.match(self.__pattern_2, server):
            self._http_server = server
        else:
            self._http_server = "https://" + server
        self.info = self.i()
        self.mi = Misskey(self._http_server, self.__token)

    def i(self):
        
        class i:
            pass
        
        with httpx.Client() as client:
            r = client.post(self._http_server + "/api/i", json={
                "i" : self.__token,
            })
            r = r.json()
            inf = i()
            inf.id = r["id"]
            inf.name = r["name"]
            inf.username = r["username"]
            inf.flags = {"cat": r["isCat"], "bot": r["isBot"]}
            inf.stat = r["onlineStatus"]
            inf.desc = r["description"]
            return inf
    
    def run(self):
        async def runner(self):
            self.__ws = await websockets.connect(f'{self.__server}/streaming?i={self.__token}')
            try:
                await self.on_ready()
            except AttributeError:
                pass
            while True:
                response = await self.__ws.recv()
                response = json.loads(response)
                try:
                    if response["body"]["type"] == "note":
                        if self.info.id in response["body"]["body"]["mentions"]:
                            try:
                                ctx = self.context()
                                ctx.note.id = response["body"]["body"]["id"]
                                ctx.author.id = response["body"]["body"]["userId"]
                                if not response["body"]["body"]["user"]["name"] == '':
                                    ctx.author.name = response["body"]["body"]["user"]["name"]
                                else:
                                    ctx.author.name = "null"
                                ctx.author.username = response["body"]["body"]["user"]["username"]
                                ctx.reactions = response["body"]["body"]["reactions"]
                                ctx.files = response["body"]["body"]["files"]
                                ctx.fileId = response["body"]["body"]["fileIds"]
                                ctx.reply.id = response["body"]["body"]["replyId"]
                                ctx.renote.id = response["body"]["body"]["renoteId"]
                                ctx.channel.type = response["body"]["id"]
                                try:
                                    ctx.mention = response["body"]["body"]["mentions"]
                                except KeyError:
                                    ctx.mention = None
                                if response["body"]["body"]["user"]["host"] is not None:
                                    ctx.author.host = response["body"]["body"]["user"]["host"]
                                    ctx.author.host.name = response["body"]["body"]["user"]["instance"]["name"]
                                    ctx.author.host.software = response["body"]["body"]["user"]["instance"]["softwareName"]
                                    ctx.author.host.softwareversion = response["body"]["body"]["user"]["instance"]["softwareVersion"]
                                    ctx.author.host.icon = response["body"]["body"]["user"]["instance"]["iconUrl"]
                                    ctx.author.host.favicon = response["body"]["body"]["user"]["instance"]["faviconUrl"]
                                    ctx.author.host.color = response["body"]["body"]["user"]["instance"]["themeColor"]
                                    ctx.uri = response["body"]["body"]["uri"]
                                    ctx.url = response["body"]["body"]["url"]
                                else:
                                    ctx.author.host = None
                                command = str(response["body"]["body"]["text"]).replace("@" + str(self.info.username), "").split()
                                await self.on_command(ctx, command)
                            except AttributeError as e:
                                pass
                        else:
                            try:
                                ctx = self.context()
                                ctx.note.id = response["body"]["body"]["id"]
                                ctx.author.id = response["body"]["body"]["userId"]
                                if not response["body"]["body"]["user"]["name"] == '':
                                    ctx.author.name = response["body"]["body"]["user"]["name"]
                                else:
                                    ctx.author.name = "null"
                                ctx.author.username = response["body"]["body"]["user"]["username"]
                                ctx.text = response["body"]["body"]["text"]
                                ctx.reactions = response["body"]["body"]["reactions"]
                                ctx.files = response["body"]["body"]["files"]
                                ctx.fileId = response["body"]["body"]["fileIds"]
                                ctx.reply.id = response["body"]["body"]["replyId"]
                                ctx.renote.id = response["body"]["body"]["renoteId"]
                                try:
                                    ctx.mention = response["body"]["body"]["mentions"]
                                except KeyError:
                                    ctx.mention = None
                                if response["body"]["body"]["user"]["host"] is not None:
                                    ctx.author.host = response["body"]["body"]["user"]["host"]
                                    ctx.author.host.name = response["body"]["body"]["user"]["instance"]["name"]
                                    ctx.author.host.software = response["body"]["body"]["user"]["instance"]["softwareName"]
                                    ctx.author.host.softwareversion = response["body"]["body"]["user"]["instance"]["softwareVersion"]
                                    ctx.author.host.icon = response["body"]["body"]["user"]["instance"]["iconUrl"]
                                    ctx.author.host.favicon = response["body"]["body"]["user"]["instance"]["faviconUrl"]
                                    ctx.author.host.color = response["body"]["body"]["user"]["instance"]["themeColor"]
                                    ctx.uri = response["body"]["body"]["uri"]
                                    ctx.url = response["body"]["body"]["url"]
                                else:
                                    ctx.author.host = None
                                await self.on_note(ctx)
                            except AttributeError as e:
                                pass
                except KeyError:
                    pass

        asyncio.run(runner(self))

    async def send(self, message, channelId, msg_type):
        await self.__ws.send(json.dumps({"type": 'channel', "body": {"id": channelId, "type": msg_type, "body": message}}, indent=4, ensure_ascii=False))

    async def connect(self, channel):
        await self.__ws.send(json.dumps({"type": "connect", "body": {"channel": channel,"id": channel}}, indent=4, ensure_ascii=False))

    async def disconnect(self, channel):
        await self.__ws.send(json.dumps({"type": "disconnect", "body": {"id": channel}}, indent=4, ensure_ascii=False))

    async def recv(self):
        return await self.__ws.recv()