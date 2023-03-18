import argparse
import gspread
from gspread import WorksheetNotFound
import snscrape.modules.twitter as sns_twitter
from loguru import logger

SPREADSHEET_NAME = 'auto archive'
COLUMN_NAMES = {
        'screenshot': 'Screenshot',
        'title': 'Upload title',
        'url': 'Link',
        'timestamp': 'Upload timestamp',
        'duration': 'Duration',
        'status': 'Archive status',
        'archive': 'Archive location',
        'date': 'Archive date',
        'thumbnail': 'Thumbnail',
        'thumbnail_index': 'Thumbnail index',
        'replaywebpage': 'Replaywebpage',
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
        if i+1 > max_results:
            logger.debug('reached the max result of scraped tweets')
            break
        tweets.append(list(['','',tweet.url]))
    return tweets

def update_spreadsheet(username, tweets):
    """ 
    Takes a list of tweets for a user and will add them to
    the auto archive google sheet. This will update an 
    existing worksheet, or create a new one if user doesn't
    already have a worksheet.
    """
    gc = gspread.service_account()
    logger.debug('Connecting to the {} sheet'.format(SPREADSHEET_NAME))
    sheet = gc.open(SPREADSHEET_NAME)
    logger.debug('Checking for existing worksheet: {}'.format(username))
    try:
        worksheet = sheet.worksheet(username)
        logger.info('{} already has balls!  Time to fill them with some pee!'.format(username))
        logger.info('Inserting pee into balls!')
        worksheet.insert_rows(tweets,row=2, value_input_option='RAW', inherit_from_before=False)
    except WorksheetNotFound:
        logger.info('No balls found for {}.  Adding an empty set of balls for pee collection'.format(username))
        worksheet = sheet.add_worksheet(username, 1, len(COLUMN_NAMES))
        logger.debug('New worksheet for {} added with {} rows and {} columns'.format(username, worksheet.row_count, worksheet.col_count))
        heading_response = worksheet.append_row(list(COLUMN_NAMES.values()), value_input_option='RAW', insert_data_option='INSERT_ROWS')
        logger.info('Inserting pee into balls!')
        worksheet.append_rows(tweets, value_input_option='RAW', insert_data_option='INSERT_ROWS')

@logger.catch
def main():
    logger.info('Balls are empty, time for pee collection')
    args = get_argument_parser().parse_args()
    logger.info('Collecting {} gallons of pee for {}'.format(args.max_results, args.username))
    tweets = grab_tweets(args.username, args.max_results)
    logger.info('{} gallons of pee collected and ready for insertion to balls'.format(args.max_results))
    update_spreadsheet(args.username, tweets)
    logger.info('{} balls are now filled with pee!'.format(args.username))

if __name__ == '__main__':
    main()