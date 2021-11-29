import math
import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize
from vkapi import config, session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    idea = f"""
       var i = 0;
           var result = [];
               while (i < {max_count}){{
                   if ({offset}+i+100 > {count}){{
                       result.push(API.wall.get({{
                       "owner_id": "{owner_id}",
                       "domain": "{domain}",
                       "offset": "{offset} +i",
                       "count": "{count}-(i+{offset})",
                       "filter": "{filter}",
                       "extended": "{extended}",
                       "fields": "{fields}"
                    }}));
               }}
               result.push(API.wall.get({{
               "owner_id": "{owner_id}",
               "domain": "{domain}",
               "offset": "{offset} +i",
               "count": "{count}",
               "filter": "{filter}",
               "extended": "{extended}",
               "fields": "{fields}"
               }}));
               i = i + {max_count};
           }}
           return result;
       """
    data = {
        "code": idea,
        "access_token": VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
    }
    r = session.post("execute", data=data)
    if r.status_code != 200:
        raise APIError("Ошибка, code:", r.status_code)

    ans = r.json()
    if "error" in ans or not r.ok:
        raise APIError(ans["error"]["error_msg"])

    json_data = ans
    return ans["response"]["items"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    user_posts = pd.DataFrame()
    if progress is None:
        progress = lambda x: x

    for _ in progress(range(math.ceil(count / 2500))):
        user_posts = user_posts.append(
            json_normalize(
                get_posts_2500(owner_id, domain, offset, count, max_count, filter, extended, fields)
            )
        )
        time.sleep(2)
    return user_posts
