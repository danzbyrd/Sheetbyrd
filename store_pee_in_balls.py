import argparse
import gspread
import snscrape.modules.twitter as sns_twitter
from loguru import logger

COLUMN_NAMES = {
        'screenshot': 'screenshot',
        'title': 'upload title',
        'url': 'link',
        'timestamp': 'upload timestamp',
        'duration': 'duration',
        'status': 'archive status',
        'archive': 'archive location',
        'date': 'archive date',
        'thumbnail': 'thumbnail',
        'thumbnail_index': 'thumbnail index',
        'replaywebpage': 'replaywebpage',
}

def get_argument_parser():
    """
    Create the CMD line arguments
    """
    parser = argparse.ArgumentParser(description="Takes a Twitter username and will pull tweets.\nSo much pee in the balls.")
    parser.add_argument('--username', required=True, help='Twitter username')
    parser.add_argument('--max-results', type=int, default=5000, help='Number of tweets to pull (Defaults to 5000).')
    parser.add_argument('--pull-from', help="Earliest date to pull tweets from")
    
    return parser

def grab_tweets(username, max_results):
    """
    Grab the url of tweets for the given username
    """
    tweets = []
    logger.debug('scraping twitter for {} and grabbing {} tweets'.format(username, max_results))
    for i, tweet in enumerate(sns_twitter.TwitterUserScraper(username).get_items()):
        if i > max_results:
            logger.debug('reached the max result of scraped tweets')
            break
        tweets.append(tweet.url)
    return tweets

@logger.catch
def main():
    args = get_argument_parser().parse_args()
    logger.info('Collecting {} gallons of pee for {}'.format(args.max_results, args.username))
    tweets = grab_tweets(args.username, args.max_results)
    print(tweets)
    logger.info('{} gallons of pee collected and ready for swishing'.format(args.max_results))

if __name__ == '__main__':
    main()


# gc =  gspread.service_account()
# logger.info('Opening "auto archive" sheet')
# sh = gc.open('auto archive')
# logger.info('Working on JennyCohn')
# ws = sh.worksheet('JennyCohn')
# print(ws.get('A1'))