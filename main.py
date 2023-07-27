import os

import feedparser
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging
from bin import linkedin, ai
import time

log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}

load_dotenv()

log_level = os.environ.get("LOG_LEVEL", "DEBUG")

# Configure logging
logging.basicConfig(
    format=(
        "{"
        '"time":"%(asctime)s",'
        ' "name": "%(name)s",'
        ' "level": "%(levelname)s",'
        ' "message": "%(message)s"'
        "}"
    ),
    level=log_levels[log_level],
    datefmt="%Y-%m-%d %H:%M:%S",
)

check_cadence = os.environ.get("SCRIPT_CADENCE", 240000)  # minutes


def get_time_in_history():
    """
    Get the time minus the cadence.

    Returns:
        Time minus the cadence.
    """
    # Get the time minus the cadence
    time_in_history = datetime.now() - timedelta(minutes=check_cadence)

    return time_in_history


def get_posts(username):
    """
    Get posts from Medium API.

    Args:
        username: Medium username.

    Returns:
        List of posts.
    """
    pass
    # Get the data from the API
    user_response = feedparser.parse("https://medium.com/feed/@" + username)

    # Check the status
    if user_response["status"] != 200:
        raise Exception(
            "Error fetching posts from Medium! Status code: "
            + str(user_response["status"])
        )

    all_posts = []

    for post in user_response["entries"]:
        title = post["title"]
        link = post["link"]
        publish_date = post["published"]
        content_html = post["content"][0]["value"]
        all_posts.append(
            {
                "title": title,
                "link": link,
                "publish_date": publish_date,
                "content_html": content_html,
            }
        )

    return all_posts


def find_posts_since_cadence(posts, cadence):
    """
    Find posts since the cadence.

    Args:
        posts: List of posts.
        cadence: Cadence to check for.

    Returns:
        List of posts since the cadence.
    """
    # Find the posts since the cadence
    posts_since_cadence = []

    for post in posts:
        logging.debug("Processing post: " + post["title"])
        # Get time since publish_date in minutes
        publish_date = post["publish_date"]
        publish_date = datetime.strptime(publish_date, "%a, %d %b %Y %H:%M:%S %Z")

        time_since_publish_date = datetime.now() - publish_date

        time_delta_minutes = int(time_since_publish_date.total_seconds() / 60)

        if time_delta_minutes < cadence:
            posts_since_cadence.append(post)

    return posts_since_cadence


def main():
    """
    Main function.

    Returns:
        True if successful, False otherwise.
    """
    # Get the posts
    try:
        posts = get_posts(os.environ.get("MEDIUM_USERNAME"))
    except Exception as error_message:
        logging.error("Failed!", str(error_message))
        sys.exit(1)

    # Find the posts since the cadence
    try:
        posts_since_cadence = find_posts_since_cadence(posts, check_cadence)
    except Exception as error_message:
        logging.error("Failed!", str(error_message))
        sys.exit(1)

    if len(posts_since_cadence) == 0:
        logging.info("No new posts since last check.")
        logging.info("Nothing to do, exiting..")
        sys.exit(0)

    # Print the posts
    logging.info(
        "Found %s new posts since %s",
        str(len(posts_since_cadence)),
        str(get_time_in_history()),
    )

    for post in posts_since_cadence:
        logging.info("Processing %s", post["title"])

        # Get summary
        try:
            summary = ai.get_summary(post["content_html"])
            print(summary)
        except Exception as error_message:
            logging.error(str(error_message))
            sys.exit(1)

        # Linkedin
        if os.environ.get("ENABLE_LINKEDIN") != "false":
            logging.debug("Linkedin enabled.")
            try:
                linkedin.create_article(post, os.environ.get("LINKEDIN_ACCESS_TOKEN"))
            except Exception as error_message:
                logging.error("Failed!", str(error_message))
                sys.exit(1)

        # Sleep 10 seconds
        logging.debug("Sleeping for 10 seconds...")
        time.sleep(10)

    return True


if __name__ == "__main__":
    main()
