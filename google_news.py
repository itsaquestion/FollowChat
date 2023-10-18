from GoogleNews import GoogleNews
import pandas as pd

import functools


def get_news_from_media(keywords, media):
    """从指定媒体抓取新闻

    >>> len(get_news_from_media('tech news','BBC')) > 0
    True
    >>> len(get_news_from_media('tech news','Reuters')) > 0
    True
    """
    googlenews = GoogleNews(period='2d')

    googlenews.search(media + ' ' + keywords)

    df = pd.DataFrame(googlenews.results())
    
    result = df.query(f'date.str.contains("hours") and media.str.contains("{media}")')[
        ['date','datetime','title', 'link']]

    return result


get_news_bbc = functools.partial(get_news_from_media, media='BBC')

get_news_reuters = functools.partial(get_news_from_media, media='Reuters')

get_news_scmp= functools.partial(get_news_from_media, media='South China Morning Post')

if __name__ == "__main__":
    #print(get_news_bbc('china news').head())
    #print(get_news_reuters('china news').head())
    print(get_news_scmp('china news').head().drop('link',axis=1))