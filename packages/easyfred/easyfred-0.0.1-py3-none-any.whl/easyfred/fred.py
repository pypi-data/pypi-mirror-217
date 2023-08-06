# fred.py

import requests
import json
import pandas as pd

class Fred:
    def __init__(self, api_key):

        """
        Initialize the Fred class with an API key.

        """

        self.api_key = api_key
        self.base_url = 'https://api.stlouisfed.org/fred/'

    def json_series(self, series_id):

        """
        Retrieve JSON data for a specified FRED series.

        Args:
        - series_id (str): The ID of the FRED series to retrieve.

        Returns:
        - data (dict): JSON data for the specified FRED series.
        """

        url = self.base_url + 'series/observations?series_id=' + series_id + '&api_key=' + self.api_key + '&file_type=json'
        response = requests.get(url)
        data = json.loads(response.text)
        return data
    
    def get_table(self, series_id):

        """
        Retrieve data for a specified FRED series and return as a Pandas DataFrame.

        Args:
        - series_id (str): The ID of the FRED series to retrieve.

        Returns:
        - df (pd.DataFrame): Data for the specified FRED series as a Pandas DataFrame.
        """

        data = self.json_series(series_id)
        df = pd.json_normalize(data['observations'])
        return df

    def search_and_get_all_series_ids(self, search_text=None, tag=None, start_date=None, end_date=None):

        """
        Search for FRED series that match specified criteria and retrieve their series IDs.

        Args:
        - search_text (str, optional): Text to search for in series titles and descriptions.
        - tag (str, optional): Tag to filter series by.
        - start_date (str, optional): Start date of observations to filter series by (YYYY-MM-DD).
        - end_date (str, optional): End date of observations to filter series by (YYYY-MM-DD).

        Returns:
        - series_ids (list): List of series IDs for the matching FRED series.
        """

        series_ids = []
        url = self.base_url + 'series/search?api_key=' + self.api_key
        if search_text:
            url += '&search_text=' + search_text.replace(' ', '+')
        if tag:
            url += '&tag=' + tag.replace(' ', '+')
        if start_date:
            url += '&observation_start=' + start_date
        if end_date:
            url += '&observation_end=' + end_date
        url += '&file_type=json'
        response = requests.get(url)
        data = json.loads(response.text)
        if 'seriess' in data:
            seriess = data['seriess']
            for series in seriess:
                series_ids.append(series['id'])
        return series_ids
    
    def search_and_get_all_series_metadata(self, search_text=None, search_type=None, realtime_start=None, realtime_end=None,
                                      limit=None, offset=None, order_by=None, sort_order=None,
                                      filter_variable=None, filter_value=None, tag_names=None, exclude_tag_names=None):
        
        """
        Search for FRED series that match specified criteria and retrieve their metadata as a Pandas DataFrame.

        Args:
        - search_text (str, optional): Text to search for in series titles and descriptions.
        - search_type (str, optional): Type of search to perform (e.g., "full_text", "series_id", "release_id").
        - realtime_start (str, optional): Start date of realtime period to filter series by (YYYY-MM-DD).
        - realtime_end (str, optional): End date of realtime period to filter series by (YYYY-MM-DD).
        - limit (int, optional): Maximum number of results to return.
        - offset (int, optional): Number of results to skip before starting to return data.
        - order_by (str, optional): Field to order results by.
        - sort_order (str, optional): Sort order for results (either "asc" or "desc").
        - filter_variable (str, optional): Variable to filter series by.
        - filter_value (str, optional): Value to filter series by.
        - tag_names (str, optional): Names of tags to filter series by (separated by commas).
        - exclude_tag_names (str, optional): Names of tags to exclude from filtered series (separated by commas).

        Returns:
        - df (pd.DataFrame): Metadata for the matching FRED series as a Pandas DataFrame.
        """
        
        url = self.base_url + 'series/search?api_key=' + self.api_key
        if search_text:
            url += '&search_text=' + search_text.replace(' ', '+')
        if search_type:
            url += '&search_type=' + search_type
        if realtime_start:
            url += '&realtime_start=' + realtime_start
        if realtime_end:
            url += '&realtime_end=' + realtime_end
        if limit:
            url += '&limit=' + str(limit)
        if offset:
            url += '&offset=' + str(offset)
        if order_by:
            url += '&order_by=' + order_by
        if sort_order:
            url += '&sort_order=' + sort_order
        if filter_variable:
            url += '&filter_variable=' + filter_variable
        if filter_value:
            url += '&filter_value=' + filter_value
        if tag_names:
            url += '&tag_names=' + tag_names
        if exclude_tag_names:
            url += '&exclude_tag_names=' + exclude_tag_names
        url += '&file_type=json'
        response = requests.get(url)
        data = json.loads(response.text)
        data_frames = []
        if 'seriess' in data:
            seriess = data['seriess']
            for series in seriess:
                series_info = {}
                series_info['id'] = series.get('id', None)
                series_info['realtime_start'] = series.get('realtime_start', None)
                series_info['realtime_end'] = series.get('realtime_end', None)
                series_info['title'] = series.get('title', None)
                series_info['observation_start'] = series.get('observation_start', None)
                series_info['observation_end'] = series.get('observation_end', None)
                series_info['frequency'] = series.get('frequency', None)
                series_info['units'] = series.get('units', None)
                series_info['units_short'] = series.get('units_short', None)
                series_info['seasonal_adjustment'] = series.get('seasonal_adjustment', None)
                series_info['seasonal_adjustment_short'] = series.get('seasonal_adjustment_short', None)
                series_info['last_updated'] = series.get('last_updated', None)
                series_info['popularity'] = series.get('popularity', None)
                series_info['group_popularity'] = series.get('group_popularity', None)
                series_info['notes'] = series.get('notes', None)
                data_frame = pd.DataFrame([series_info])
                data_frames.append(data_frame)
        if data_frames:
            return pd.concat(data_frames, ignore_index=True)
        else:
            return pd.DataFrame()
        
    def get_info(self):
        """
        Get all the methods in the Fred class and their descriptions.

        Returns:
        - methods (list): A list of dictionaries with method names and some info.
        """
        methods = []
        for name in dir(self):
            attr = getattr(self, name)
            if callable(attr) and not name.startswith('__'):
                docstring = attr.__doc__ or ''
                method_info = {
                    'Method': name,
                    'Description': '',
                    'Arguments': '',
                    'Returns': ''
                }
                desc_start = docstring.find('Args:') or len(docstring)
                desc = docstring[:desc_start].strip().replace('\n', ', ').strip(', ')
                if desc and not desc.endswith(','):
                    desc += ','
                args_start = docstring.find('Args:')
                args_end = docstring.find('Returns:') or len(docstring)
                args = docstring[args_start:args_end].strip().replace('Args:', '').strip().replace('- ', '').strip(', ').replace('\n', ', ').strip(', ')
                returns_start = docstring.find('Returns:')
                returns = docstring[returns_start:].strip().replace('Returns:', '').strip().replace('- ', '').strip(', ').replace('\n', ', ').strip(', ')
                method_info['Description'] = desc
                method_info['Arguments'] = args
                method_info['Returns'] = returns
                methods.append(method_info)
        methods = [m for m in methods if m['Method'] != 'get_info']
        return methods