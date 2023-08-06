import platform
import re

from httpx import Client

from twitter.util import find_key, build_params

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


def search(client: Client, query: str, category: str, limit: int):
    def get_cursor(data: list[dict]):
        for e in find_key(data, 'content'):
            if e.get('cursorType') == 'Bottom':
                return e['value']

    params = {
        'variables': {
            'rawQuery': query,
            'count': 20,
            'querySource': 'typed_query',
            'product': category,  # Top Latest People Photos Videos
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

    r = client.get(
        f'https://twitter.com/i/api/graphql/nK1dw4oV3k4w5TdtcAdSww/SearchTimeline',
        params=build_params(params),
    )
    data = r.json()
    cursor = get_cursor(data)
    entries = [y for x in find_key(data, 'entries') for y in x if re.search(r'^(tweet|user)-', y['entryId'])]

    total = set()
    res = [*entries]
    while True:
        if cursor:
            params['variables']['cursor'] = cursor
        r = client.get(
            f'https://twitter.com/i/api/graphql/nK1dw4oV3k4w5TdtcAdSww/SearchTimeline',
            params=build_params(params),
        )
        data = r.json()
        cursor = get_cursor(data)
        entries = [y for x in find_key(data, 'entries') for y in x if re.search(r'^(tweet|user)-', y['entryId'])]
        res.extend(entries)
        unq = set(find_key(entries, 'entryId'))
        total |= unq
        print(f'{len(total) = }')
        if len(total) >= limit:
            return res


def main():
    client = Client(
        cookies={
            'guest_id_marketing': 'v1%3A168831467118226516',
            'guest_id_ads': 'v1%3A168831467118226516',
            'guest_id': 'v1%3A168831467118226516',
            'gt': '1675539289323732992',
            '_twitter_sess': 'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCD90ZReJAToMY3NyZl9p%250AZCIlY2VmODY5NTk5MDY3ZGM3MjE0OWEyNGYzYmU1YWU1MjQ6B2lkIiUwZDZh%250AMDNjMzI0MDI0ZjA0Y2Y3ZDljYzBkZGIwZmRmNw%253D%253D--3180abacfe29ca6cbd1242569856bfa6182c977c',
            'kdt': 'zuRXkC6kZtCny3QK9P36h0QjflevUjimKXEsM3k2',
            'auth_token': 'e83fb0a587c38a700d2cd979111824332db1b27d',
            'ct0': 'd40a5beec7fd8d1bf3dff79a574865021637e6e0e09cedb768af0d4fec2c43ccd90f1ae9cdf65ad565288f8b47700dc63a01d138405dc86d2074cc654e5d5cc34d8a1cc95dbc79a9af92eae70ce30c7a',
            'lang': 'en',
            'twid': 'u%3D1669836662040596482',
            'att': '1-jDRImjDf7eGHZe4JgFHSC60myM7BmNwNVbyXrcfr',
            'personalization_id': '"v1_QdQg2g93s2iVDOIUSYEAuw=="',
        },
        headers={
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'referer': 'https://twitter.com/search?q=match%20all%20of%20these%20%22match%20my%20exact%20phrase%22%20(match%20OR%20all%20OR%20of%20OR%20these)%20-do%20-not%20-include%20-this%20(%23hashtag1%20OR%20%23hashtag2)%20(from%3AthisAccount%20OR%20from%3AthatAccount)%20(to%3AtoThisAccount%20OR%20to%3AtoThatAccount)%20(%40mentioningThisAccount%20OR%20%40mentioningThatAccount)%20min_replies%3A11%20min_faves%3A222%20min_retweets%3A333%20lang%3Aen%20until%3A2023-02-12%20since%3A2023-01-01&src=typed_query',
            'sec-ch-ua': '"Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-client-uuid': '267346b7-e0c7-478f-8ef6-e24d8a575ead',
            'x-csrf-token': 'd40a5beec7fd8d1bf3dff79a574865021637e6e0e09cedb768af0d4fec2c43ccd90f1ae9cdf65ad565288f8b47700dc63a01d138405dc86d2074cc654e5d5cc34d8a1cc95dbc79a9af92eae70ce30c7a',
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
        })

    # response = requests.get(
    #     'https://twitter.com/i/api/graphql/nK1dw4oV3k4w5TdtcAdSww/SearchTimeline?variables=%7B%22rawQuery%22%3A%22match%20all%20of%20these%20%5C%22match%20my%20exact%20phrase%5C%22%20(match%20OR%20all%20OR%20of%20OR%20these)%20-do%20-not%20-include%20-this%20(%23hashtag1%20OR%20%23hashtag2)%20(from%3AthisAccount%20OR%20from%3AthatAccount)%20(to%3AtoThisAccount%20OR%20to%3AtoThatAccount)%20(%40mentioningThisAccount%20OR%20%40mentioningThatAccount)%20min_replies%3A11%20min_faves%3A222%20min_retweets%3A333%20lang%3Aen%20until%3A2023-02-12%20since%3A2023-01-01%22%2C%22count%22%3A20%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Top%22%7D&features=%7B%22rweb_lists_timeline_redesign_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D&fieldToggles=%7B%22withArticleRichContentState%22%3Afalse%7D',
    #     cookies=cookies,
    #     headers=headers,
    # )
    res = search(client, 'argentina', 'Top', 60)
    print(res)


if __name__ == '__main__':
    main()
