from requests import get, post


class NoidAPI:
    
    def __init__(self) -> None:
        self.api_key = 'api-key'
        self.base_url = 'https://api.xgorn.pp.ua'
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        kwargs['api_key'] = self.api_key
        if self.api_key == 'api-key':
            return {'error': True, 'message': 'Invalid API key'}
        if method == 'get':
            return get(self.base_url+endpoint, params=kwargs).json()
        elif method == 'post':
            return post(self.base_url+endpoint, data=kwargs).json()
        else:
            return {'error': True, 'message': 'Invalid method'}
    
    def ouo_bypass(self, url: str) -> dict:
        return self.make_request('get', '/ouo_bypass', url=url)
    
    def mirrored_bypass(self, url: str, host: str) -> dict:
        return self.make_request('get', '/mirrored_bypass', url=url, host=host)
    
    def tiktok_scrape(self, url: str) -> dict:
        return self.make_request('get', '/tiktok_scrape', url=url)
    
    def facebook_scrape(self, url: str) -> dict:
        return self.make_request('get', '/facebook_scrape', url=url)
    
    def instagram_scrape(self, url: str) -> dict:
        return self.make_request('get', '/instagram_scrape', url=url)
    
    def instagram_scrapev2(self, url: str) -> dict:
        return self.make_request('get', '/instagram_scrapev2', url=url)

    def twitter_scrape(self, url: str) -> dict:
        return self.make_request('get', '/twitter_scrape', url=url)
    
    def twitter_scrapev2(self, url: str) -> dict:
        return self.make_request('get', '/twitter_scrapev2', url=url)
    
    def likee_scrape(self, url: str) -> dict:
        return self.make_request('get', '/likee_scrape', url=url)
    
    def pinterest_scrape(self, url: str) -> dict:
        return self.make_request('get', '/pinterest_scrape', url=url)
    
    def pinterest_scrapev2(self, url: str) -> dict:
        return self.make_request('get', '/pinterest_scrapev2', url=url)
    
    def terabox_scrape(self, url: str) -> dict:
        return self.make_request('get', '/terabox_scrape', url=url)
    
    def gofile_scrape(self, url: str) -> dict:
        return self.make_request('get', '/gofile_scrape', url=url)
    
    def krakenfiles_scrape(self, url: str) -> dict:
        return self.make_request('get', '/krakenfiles_scrape', url=url)
    
    def yifysubtitles_scrape(self, imdb_id: str, lang: str) -> dict:
        return self.make_request('get', '/yifysubtitles_scrape', imdb_id=imdb_id, lang=lang)
    
    def filelions_scrape(self, url: str) -> dict:
        return self.make_request('get', '/filelions_scrape', url=url)
    
    def streamwish_scrape(self, url: str) -> dict:
        return self.make_request('get', '/streamwish_scrape', url=url)
    
    def srt_translate(self, url: str, source_lang: str, dest_lang: str) -> dict:
        return self.make_request('get', '/srt_translate', url=url, source_lang=source_lang, dest_lang=dest_lang)
    
    def shazam_music_find(self, url: str, type_: str) -> dict:
        return self.make_request('get', '/shazam_music_find', url=url, type=type_)