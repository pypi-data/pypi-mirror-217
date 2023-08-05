import requests
import json
import os

class Collabim:
    BASE_URL = 'https://api.oncollabim.com'
    ONE_TIME_ANALYSES_KEYWORD_MEASURING_URL = '/ota/keyword-measuring'
    GET_PROJECT_NFO_BY_ID = '/projects/'
    GET_PROJECTS_LIST = '/projects'
    GET_WIDGETS = '/projects/%s/widget/fullWidget'
    GET_WIDGETS_JSON = '/projects/%s/widget/fullWidget/json'
    GET_ACTIVITIES = '/activities?projectId=%s'
    GET_ACTIVITY = '/activities/%s'
    DELETE_ACTIVITY = '/activities/%s'
    POST_ACTIVITY = '/activities'
    PUT_ACTIVITY = '/activities/%s'
    GET_KEYWORDS = '/keywords?projectId=%s'
    GET_KEYWORDS_POSITION = '/keyword-positions?projectId=%s'
    GET_KEYWORDS_POSITION_AGGREGATED = '/aggregated-keywords-positions?projectId=%s'
    GET_POSITION_DISTRIBUTION = '/position-distribution?projectId=%s'
    GET_INDEXED_PAGES = '/indexed-pages?projectId=%s'
    GET_MARKET_SHARE = '/market-share?projectId=%s'

    headers = {
        'Accept':'application/collabim+json',
        'Content-Type':'application/json'
    }

    def __init__(self, config_file='config.ini', headers=[]):
        self.config = self._parse_ini(config_file)
        if 'COLLABIM' not in self.config or 'apiKey' not in self.config['COLLABIM']:
            raise Exception("apiKey is required in {config_file} section [COLLABIM], you can request it on https://collabim.cz/?promoCode=mRfeciXH1V\n")
        else:
            self.api_key = self.config['COLLABIM']['apiKey']
        self.headers.update(headers)
        self.session = requests.Session()

    def _parse_ini(self, config_file):
        import configparser
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            return config
        else:
            raise Exception(f"{config_file} not found")

    def authenticate(self):
        if self.api_key:
            self.headers['Authorization'] = self.api_key
            return True
        return False

    def _get_data(self, response):
        if response.status_code == 200:
            json_response = response.json()
            if 'data' in json_response:
                return json_response['data']
            elif 'message' in json_response:
                raise Exception(json_response['message'])
            else:
                return json_response
        else:
            response.raise_for_status()

    def _get_pure_data(self, response):
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def _request(self, method, url, data=None):
        response = self.session.request(method, self.BASE_URL + url, headers=self.headers, json=data)
        return response

    def project_get_info_by_id(self, id):
        response = self._request('GET', self.GET_PROJECT_NFO_BY_ID + str(id))
        return self._get_data(response)

    def project_get_widgets_HTML(self, project_id):
        response = self._request('GET', self.GET_WIDGETS % project_id)
        return self._get_pure_data(response)

    def project_get_widgets_JSON(self, project_id):
        response = self._request('GET', self.GET_WIDGETS_JSON % project_id)
        return self._get_data(response)

    def project_get_list(self):
        response = self._request('GET', self.GET_PROJECTS_LIST)
        return self._get_data(response)

    def activity_get_list(self, project_id):
        response = self._request('GET', self.GET_ACTIVITIES % project_id)
        return self._get_data(response)

    def activity_get_info_by_id(self, activity_id):
        response = self._request('GET', self.GET_ACTIVITY % activity_id)
        return self._get_data(response)

    def activity_delete_by_id(self, activity_id):
        response = self._request('DELETE', self.DELETE_ACTIVITY % activity_id)
        return self._get_data(response)

    def activity_create(self, data):
        response = self._request('POST', self.POST_ACTIVITY, data)
        return self._get_data(response)

    def activity_update(self, activity_id, data):
        response = self._request('PUT', self.PUT_ACTIVITY % activity_id, data)
        return self._get_data(response)

    def keyword_get_list(self, project_id):
        response = self._request('GET', self.GET_KEYWORDS % project_id)
        return self._get_data(response)

    def keyword_get_positions(self, project_id):
        response = self._request('GET', self.GET_KEYWORDS_POSITION % project_id)
        return self._get_data(response)

    def keyword_get_positions_aggregated(self, project_id):
        response = self._request('GET', self.GET_KEYWORDS_POSITION_AGGREGATED % project_id)
        return self._get_data(response)

    def position_get_distribution(self, project_id):
        response = self._request('GET', self.GET_POSITION_DISTRIBUTION % project_id)
        return self._get_data(response)

    def indexed_pages_get_list(self, project_id):
        response = self._request('GET', self.GET_INDEXED_PAGES % project_id)
        return self._get_data(response)

    def market_share_get_info(self, project_id):
        response = self._request('GET', self.GET_MARKET_SHARE % project_id)
        return self._get_data(response)
