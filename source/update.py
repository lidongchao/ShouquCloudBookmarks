# encoding: utf-8

import time
from workflow import web, Workflow

def get_recent_markbooks(userId):
    """Retrieve recent markbooks from shouqu.me
    Return a list of markbooks dictionaries.

    """
    # Generate URL to post
    lastupdataTime = str(int(time.time()*1000))
    url = "https://api.shouqu.me/api_service/api/v1/mark/webList"
    data = dict()
    data['userId'] = userId
    data['lastupdataTime'] = lastupdataTime
    data['pageNo'] = 1
    data['pageSize'] = 30
    data['sort'] = 'desc'
    data['renderType'] = 0
    headers = dict()
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

    # Generate a post
    r = web.post(url, data=data, headers=headers)

    # Throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by shouqu.me and extract the markbooks
    result = r.json()
    markbooks = result['data']['list']
    return markbooks


def main(wf):
    userId = wf.settings.get('userId', None)

    # Retrieve markbooks from cache if available and no more than 10 minutes old
    def wrapper():
        return get_recent_markbooks(userId)

    markbooks = wf.cached_data('markbooks', wrapper, max_age=600)
    # Record our progress in the log file
    wf.logger.debug('{} bookmarks cached'.format(len(markbooks)))


if __name__ == u"__main__":
    wf = Workflow()
    wf.run(main)