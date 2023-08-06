import json
import aiohttp

from typing import Union
from amiyabot import log


class HttpRequests:
    success = [200, 204]
    async_success = [201, 202, 304023, 304024]

    @classmethod
    async def request(cls,
                      url: str,
                      method: str = 'post',
                      request_name: str = None,
                      ignore_error: bool = False,
                      **kwargs):
        try:
            request_name = (request_name or method).upper()

            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.request(method, url, **kwargs) as res:
                    if res.status in cls.success:
                        return await res.text()
                    if res.status in cls.async_success:
                        return ''
                    if not ignore_error:
                        log.error(f'bad to request <{url}>[{request_name}]. Got code {res.status}')
        except aiohttp.ClientConnectorError:
            if not ignore_error:
                log.error(f'fail to request <{url}>[{request_name}]')
        except Exception as e:
            if not ignore_error:
                log.error(e)

    @classmethod
    async def get(cls,
                  interface: str,
                  **kwargs):
        return await cls.request(interface, 'get', **kwargs)

    @classmethod
    async def post(cls,
                   interface: str,
                   payload: Union[dict, list] = None,
                   headers: dict = None,
                   **kwargs):
        _headers = {
            'Content-Type': 'application/json',
            **(headers or {})
        }
        _payload = {
            **(payload or {})
        }
        return await cls.request(interface, 'post', data=json.dumps(_payload), headers=_headers, **kwargs)

    @classmethod
    async def post_form(cls,
                        interface: str,
                        payload: dict = None,
                        headers: dict = None,
                        **kwargs):
        _headers = {
            **(headers or {})
        }

        data = cls.__build_form_data(payload)

        return await cls.request(interface, 'post', 'post-form', data=data, headers=_headers, **kwargs)

    @classmethod
    async def post_upload(cls,
                          interface: str,
                          file: bytes,
                          file_field: str = 'file',
                          payload: dict = None,
                          headers: dict = None,
                          **kwargs):
        _headers = {
            **(headers or {})
        }

        data = cls.__build_form_data(payload)
        data.add_field(file_field,
                       file,
                       content_type='application/octet-stream')

        return await cls.request(interface, 'post', 'post-upload', data=data, headers=_headers, **kwargs)

    @classmethod
    def __build_form_data(cls, payload: dict):
        data = aiohttp.FormData()

        for field, value in (payload or {}).items():
            if value is None:
                continue
            if type(value) in [dict, list]:
                value = json.dumps(value, ensure_ascii=False)
            data.add_field(field, value)

        return data


http_requests = HttpRequests
