import json
import os
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request

"""
official api documentation:
https://github.com/ToontownRewritten/api-doc/blob/master/login.md
https://github.com/ToontownRewritten/api-doc/blob/master/invasions.md
"""

INVASIONS_API_URL = 'https://www.toontownrewritten.com/api/invasions?format=json'
LOGIN_API_URL = 'https://www.toontownrewritten.com/api/login?format=json'

if sys.platform == 'darwin':
    TOONTOWN_LIBRARY_PATH = os.path.join(
        os.path.expanduser('~'), 'Library',
        'Application Support', 'Toontown Rewritten',
    )
    TOONTOWN_ENGINE_DEFAULT_PATH = os.path.join(
        TOONTOWN_LIBRARY_PATH,
        'Toontown Rewritten',
    )
else:
    TOONTOWN_LIBRARY_PATH = None
    TOONTOWN_ENGINE_DEFAULT_PATH = None


def start_engine(engine_path, gameserver, playcookie, **kwargs):
    env = {
        'TTR_GAMESERVER': gameserver,
        'TTR_PLAYCOOKIE': playcookie,
    }
    if sys.platform == 'darwin':
        env['DYLD_LIBRARY_PATH'] = os.path.join(
            TOONTOWN_LIBRARY_PATH,
            'Libraries.bundle',
        )
        env['DYLD_FRAMEWORK_PATH'] = os.path.join(
            TOONTOWN_LIBRARY_PATH,
            'Frameworks',
        )
    return subprocess.Popen(
        args=[engine_path],
        cwd=os.path.dirname(engine_path),
        env=env,
        **kwargs,
    )


def api_request(url, params=None, validate_ssl_cert=True):
    resp = urllib.request.urlopen(
        url=url,
        data=urllib.parse.urlencode(params).encode('ascii')
            if params else None,
        context=None if validate_ssl_cert
            else ssl._create_unverified_context(),
    )
    return json.loads(resp.read().decode('ascii'))


class LoginSuccessful:

    def __init__(self, playcookie, gameserver):
        self.playcookie = playcookie
        self.gameserver = gameserver


class LoginDelayed:

    def __init__(self, queue_token):
        self.queue_token = queue_token


def login(username=None, password=None,
          queue_token=None, validate_ssl_cert=True):
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
        validate_ssl_cert=validate_ssl_cert,
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


def launch(engine_path, username, password, validate_ssl_certs=True):
    result = login(
        username=username,
        password=password,
        validate_ssl_cert=validate_ssl_certs,
    )
    if isinstance(result, LoginDelayed):
        result = login(
            queue_token=result.queue_token,
            validate_ssl_cert=validate_ssl_certs,
        )
    if isinstance(result, LoginSuccessful):
        p = start_engine(
            engine_path=engine_path,
            gameserver=result.gameserver,
            playcookie=result.playcookie,
        )
        p.wait()
    else:
        raise Exception(repr(result))
