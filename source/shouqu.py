# encoding: utf-8

import sys, time
import argparse
from workflow import Workflow, web, ICON_WEB, ICON_WARNING, ICON_INFO, ICON_FAVORITE
from workflow.background import run_in_background, is_running



def search_key_for_markbooks(markbook):
    """Generate a string search key for a markbook"""
    elements = []
    
    elements.append(markbook['title'] if markbook['title'] else " ")  # title of markbook
    elements.append(markbook['introduct'] if markbook['introduct'] else " ")  # introduction of markbook
    elements.append(markbook['sourceName'] if markbook['sourceName'] else " ")  # source name of markbook
    elements.append(markbook['url'] if markbook['url'] else " ")  # url of markbook

    return u' '.join(elements)

def saver(wf, saved):

    # Generate URL to post
    userId = wf.settings.get('userId', None)
    url = "https://api.shouqu.me/api_service/api/v1/mark/add"

    if not saved.startswith('http'):
        saved = u'http://' + saved

    
    params = dict()
    params['userId'] = userId
    params['channel'] = 11
    params['url'] = saved
    headers = dict()
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

    # Generate a get
    r = web.get(url, params=params, headers=headers)

    # Throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    # Parse the JSON returned by shouqu.me and extract the result
    result = r.json()
    if result['code'] == 200:
        wf.logger.debug('bookmark {} saved'.format(saved))
        print('[Succeed]: Bookmark was saved on Shouqu')
    else:
        wf.logger.debug('bookmark {} not saved'.format(saved))
        print('[Failed]: ' + result['message']).encode('utf-8')



def main(wf):

    # build argument parser to parse script args and collect their values
    parser = argparse.ArgumentParser()
    # add an optional (nargs='?') --setid argument and save its
    # value to 'userId' (dest). This will be called from a separate "Run Script"
    # action with the userId
    parser.add_argument('--setid', dest='userId', nargs='?', default=None)
    # similarly add an optional --saving argument and save its value to 'saving'
    parser.add_argument('--saving', dest='saving', nargs='?', default=None)
    # similarly add an optional --saved argument and save its value to 'saved'
    parser.add_argument('--saved', dest='saved', nargs='?', default=None)
    # add an optional query and save it to 'query'
    parser.add_argument('query', nargs='?', default=None)
    # parse the script's arguments
    args = parser.parse_args(wf.args)


    ####################################################################
    # Save the provided userId
    ####################################################################

    # decide what to do based on arguments
    if args.userId:  # Script was passed a userId
        # save the userId
        wf.settings['userId'] = args.userId
        wf.logger.debug('userId {} saved'.format(args.userId))
        print("[Succeed]: Your Shouqu user id {} was saved".format(args.userId))
        return 0  # 0 means script exited cleanly

    ####################################################################
    # Check that we have an API key saved
    ####################################################################
    userId = wf.settings.get('userId', None)
    if not userId:  # userId has not yet been set
        wf.add_item('No user id set.',
                    'Please use sqsetid to set your Shouqu user id.',
                    valid=False,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    ####################################################################
    # Add shouqu bookmarks
    ####################################################################
    if args.saving:
        wf.add_item('Save bookmark {} on Shouqu'.format(args.saving),
                    'Copy website URL on this and hit ENTER',
                    arg=args.saving,
                    valid=True,
                    icon=ICON_FAVORITE)
        wf.send_feedback()
        return 0

    if args.saved:
        saver(wf, args.saved)
        return 0



    ####################################################################
    # View/filter shouqu bookmarks
    ####################################################################
    
    query = args.query

    # Get bookmarks from cache. Set `data_func` to None, as we don't want to
    # update the cache in this script and `max_age` to 0 because we want
    # the cached data regardless of age
    markbooks = wf.cached_data('markbooks', None, max_age=0)

    # Start update script if cached data is too old (or doesn't exist)
    if not wf.cached_data_fresh('markbooks', max_age=600):
        cmd = ['/usr/bin/python', wf.workflowfile('update.py')]
        run_in_background('update', cmd)

    # Notify the user if the cache is being updated
    if is_running('update'):
        wf.add_item('Getting new bookmarks from Shouqu',
                    valid=False,
                    icon=ICON_INFO)
    

    # If script was passed a query, use it to filter markbooks
    if query and markbooks:
        markbooks = wf.filter(query, markbooks, key=search_key_for_markbooks)

    if not markbooks:  # we have no data to show, so show a warning and stop
        wf.add_item('No markbooks found, please try again', icon=ICON_WARNING)
        wf.send_feedback()
        return 0


    # Loop through the returned markbooks and add an item for each to the 
    # list of results for Alfred
    for markbook in markbooks:
        wf.add_item(title=markbook['title'],
                    subtitle=markbook['introduct'],
                    arg=markbook['url'],
                    valid=True)

    # Send the results to Alfred as XML
    wf.send_feedback()




if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))