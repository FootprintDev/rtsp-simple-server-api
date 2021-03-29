import yaml
from hashlib import sha256
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


class Source():
    record = "record"
    redirect = "redirect"
    url = ""


class SourceProtocol():
    auto = "automatic"
    udp = "udp"
    tcp = "tcp"


class PasswortManager:
    def __init__(self, passwd):
        self.passwd = passwd

    def encrypt(self):
        return "sha256:"+sha256(self.passwd.encode('utf-8')).hexdigest()

class Path(BaseModel):
    source: str
    sourceProtocol: str
    sourceOnDemand: bool
    sourceOnDemandStartTimeout: str
    sourceOnDemandCloseAfter: str
    sourceRedirect: str
    disablePublisherOverride: bool
    fallback: str
    publishUser: str
    publishPass: str
    publishIps: list
    readUser: str
    readPass: str
    readIps: list
    runOnInit: str
    runOnInitRestart: bool
    runOnDemand: str
    runOnDemandRestart: bool
    runOnDemandStartTimeout: str
    runOnDemandCloseAfter: str
    runOnPublish: str
    runOnPublishRestart: bool
    runOnRead: str
    runOnReadRestart: bool

class PathRequest(BaseModel):
    name: str
    path: Path


def read():
    with open("rtsp-simple-server-test.yml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write(data):
    with open("rtsp-simple-server-test.yml", 'w') as stream:
        try:
            stream.write(yaml.safe_dump(data))
        except yaml.YAMLError as exc:
            print(exc)

def Convert(lst): 
    it = iter(lst) 
    res_dct = dict(zip(it, it)) 
    return res_dct


app = FastAPI(
    title="RTSP Server API",
    description="This Service is to manage a RTSP Simple Server",
    version="1",)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/config/server")
async def server_config():
    return read()


@app.get("/config/paths")
async def server_paths():
    return read()['paths']

@app.post("/config/paths")
async def server_path(PathRequest: PathRequest):
    try:
        config = read()
        path = dict(PathRequest.path)
        path['publishPass'] = PasswortManager(path['publishPass']).encrypt()
        config['paths'][PathRequest.name] = path
        write(config)
        return {"success": True}
    except Exception as exc:
        return exc
