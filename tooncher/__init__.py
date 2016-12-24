import json
import os
import subprocess
import urllib.parse
import urllib.request

"""
official api documentation:
https://github.com/ToontownRewritten/api-doc/blob/master/login.md
https://github.com/ToontownRewritten/api-doc/blob/master/invasions.md
"""

INVASIONS_API_URL = 'https://www.toontownrewritten.com/api/invasions?format=json'
LOGIN_API_URL = 'https://www.toontownrewritten.com/api/login?format=json'


def start_engine(engine_path, gameserver, playcookie, **kwargs):
    return subprocess.Popen(
        args=[engine_path],
        cwd=os.path.dirname(engine_path),
        env={
            'TTR_GAMESERVER': gameserver,
            'TTR_PLAYCOOKIE': playcookie,
        },
        **kwargs,
    )


def api_request(url, params=None):
    resp = urllib.request.urlopen(
        url=url,
        data=urllib.parse.urlencode(params).encode('ascii')
            if params else None,
    )
    return json.loads(resp.read().decode('ascii'))


class LoginSuccessful:

    def __init__(self, playcookie, gameserver):
        self.playcookie = playcookie
        self.gameserver = gameserver


class LoginDelayed:

    def __init__(self, queue_token):
        self.queue_token = queue_token


def login(username=None, password=None, queue_token=None):
    if username is not None and queue_token is None:
        assert password is not None
        req_params = {
            'username': username,
            'password': password,
        }
    elif username is None and queue_token is not None:
        req_params = {
            'queueToken': queue_token,
        }
    else:
        raise Exception('either specify username or queue token')
    resp_data = api_request(
        url=LOGIN_API_URL,
        params=req_params,
    )
    if resp_data['success'] == 'true':
        return LoginSuccessful(
            playcookie=resp_data['cookie'],
            gameserver=resp_data['gameserver'],
        )
    elif resp_data['success'] == 'delayed':
        return LoginDelayed(
            queue_token=resp_data['queueToken'],
        )
    else:
        raise Exception(repr(resp_data))


def launch(engine_path, username, password):
    result = login(
        username=username,
        password=password,
    )
    if isinstance(result, LoginDelayed):
        result = login(queue_token=result.queue_token)
    if isinstance(result, LoginSuccessful):
        p = start_engine(
            engine_path=engine_path,
            gameserver=result.gameserver,
            playcookie=result.playcookie,
        )
        p.wait()
    else:
        raise Exception(repr(result))
