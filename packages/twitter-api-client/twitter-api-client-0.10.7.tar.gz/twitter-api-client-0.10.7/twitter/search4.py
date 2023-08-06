import asyncio
import logging.config
import math
import platform
import random
import re
import time
from logging import Logger
from pathlib import Path

import orjson
from httpx import AsyncClient, Client

from .constants import *
from .login import login
from .util import get_headers, find_key, build_params

reset = '\u001b[0m'
colors = [f'\u001b[{i}m' for i in range(30, 38)]

try:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        import nest_asyncio

        nest_asyncio.apply()
except:
    ...

if platform.system() != 'Windows':
    try:
        import uvloop

        uvloop.install()
    except ImportError as e:
        ...


class Search:
    def __init__(self, email: str = None, username: str = None, password: str = None, session: Client = None, **kwargs):
        self.save = kwargs.get('save', True)
        self.debug = kwargs.get('debug', 0)
        self.logger = self._init_logger(**kwargs)
        self.session = self._validate_session(email, username, password, session, **kwargs)

    def run(self, queries: list[dict], limit: int = math.inf, **kwargs):
        out = Path('data/search_results')
        out.mkdir(parents=True, exist_ok=True)
        return asyncio.run(self.process(queries, limit, out, **kwargs))

    async def process(self, queries: list[dict], limit: int, out: Path, **kwargs) -> list:
        async with AsyncClient(headers=get_headers(self.session)) as s:
            return await asyncio.gather(*(self.paginate(s, q, limit, out, **kwargs) for q in queries))

    async def paginate(self, client: AsyncClient, query: dict, limit: int, out: Path, **kwargs) -> list[dict]:
        c = colors.pop() if colors else ''
        params = {
            'variables': {
                'count': 20,
                'querySource': 'typed_query',
            },
            'features': {
                'rweb_lists_timeline_redesign_enabled': True,
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'creator_subscriptions_tweet_preview_api_enabled': True,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'responsive_web_twitter_article_tweet_consumption_enabled': False,
                'tweet_awards_web_tipping_enabled': False,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'responsive_web_media_download_video_enabled': False,
                'responsive_web_enhance_cards_enabled': False
            },
            'fieldToggles': {'withArticleRichContentState': False},
        }
        params['variables']['rawQuery'] = query['query']
        params['variables']['product'] = query['category']

        # data, entries, cursor = await self.get(client, params)
        data, entries, cursor = await self.backoff(lambda: self.get(client, params), **kwargs)

        total = set()
        res = [*entries]
        while True:
            if cursor:
                params['variables']['cursor'] = cursor

            # data, entries, cursor = await self.get(client, params)
            data, entries, cursor = await self.backoff(lambda: self.get(client, params), **kwargs)

            if len(entries) <= 2:  # just cursors
                return res

            res.extend(entries)
            unq = set(find_key(entries, 'entryId'))
            total |= unq

            if self.debug:
                self.logger.debug(f'{c}{query["query"]}{reset}')

            if len(total) >= limit:
                if self.debug:
                    self.logger.debug(
                        f'[{GREEN}success{RESET}] Returned {len(total)} search results for {c}{query["query"]}{reset}')
                return res

            if self.save:
                (out / f'{time.time_ns()}.json').write_bytes(orjson.dumps(entries))

    async def backoff(self, fn, **kwargs):
        retries = kwargs.get('retries', 3)
        for i in range(retries + 1):
            try:
                data, entries, cursor = await fn()
                ids = set(find_key(data, 'entryId'))
                if len(ids) >= 2:
                    return data, entries, cursor
            except Exception as e:
                if i == retries:
                    self.logger.debug(f'Max retries exceeded\n{e}')
                    return
                t = 2 ** i + random.random()
                self.logger.debug(f'Retrying in {f"{t:.2f}"} seconds\t\t{e}')
                # time.sleep(t)
                await asyncio.sleep(t)

    async def get(self, client: AsyncClient, params: dict) -> tuple:
        r = await client.get(
            f'https://twitter.com/i/api/graphql/nK1dw4oV3k4w5TdtcAdSww/SearchTimeline',
            params=build_params(params),
        )
        data = r.json()
        cursor = self.get_cursor(data)
        entries = [y for x in find_key(data, 'entries') for y in x if re.search(r'^(tweet|user)-', y['entryId'])]
        # add on query info
        for e in entries:
            e['query'] = params['variables']['rawQuery']
        return data, entries, cursor

    def get_cursor(self, data: list[dict]):
        for e in find_key(data, 'content'):
            if e.get('cursorType') == 'Bottom':
                return e['value']

    def _init_logger(self, **kwargs) -> Logger:
        if kwargs.get('debug'):
            cfg = kwargs.get('log_config')
            logging.config.dictConfig(cfg or LOG_CONFIG)

            # only support one logger
            logger_name = list(LOG_CONFIG['loggers'].keys())[0]

            # set level of all other loggers to ERROR
            for name in logging.root.manager.loggerDict:
                if name != logger_name:
                    logging.getLogger(name).setLevel(logging.ERROR)

            return logging.getLogger(logger_name)

    @staticmethod
    def _validate_session(*args, **kwargs):
        email, username, password, session = args

        # validate credentials
        if all((email, username, password)):
            return login(email, username, password, **kwargs)

        # invalid credentials, try validating session
        if session and all(session.cookies.get(c) for c in {'ct0', 'auth_token'}):
            return session

        # invalid credentials and session
        cookies = kwargs.get('cookies')

        # try validating cookies dict
        if isinstance(cookies, dict) and all(cookies.get(c) for c in {'ct0', 'auth_token'}):
            _session = Client(cookies=cookies, follow_redirects=True)
            _session.headers.update(get_headers(_session))
            return _session

        # try validating cookies from file
        if isinstance(cookies, str):
            _session = Client(cookies=orjson.loads(Path(cookies).read_bytes()), follow_redirects=True)
            _session.headers.update(get_headers(_session))
            return _session

        raise Exception('Session not authenticated. '
                        'Please use an authenticated session or remove the `session` argument and try again.')

    @property
    def id(self) -> int:
        """ Get User ID """
        return int(re.findall('"u=(\d+)"', self.session.cookies.get('twid'))[0])

    def save_cookies(self, fname: str = None):
        """ Save cookies to file """
        cookies = self.session.cookies
        Path(f'{fname or cookies.get("username")}.cookies').write_bytes(orjson.dumps(dict(cookies)))
