import os

import feedparser
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

check_cadence = 6000  # minutes


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
        print("Processing post: " + post["title"])
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
        print("Failed!", str(error_message))
        sys.exit(1)

    # Find the posts since the cadence
    try:
        posts_since_cadence = find_posts_since_cadence(posts, check_cadence)
    except Exception as error_message:
        print("Failed!", str(error_message))
        sys.exit(1)

    if len(posts_since_cadence) == 0:
        print("No new posts since last check.")
        print("Nothing to do, exiting..")
        sys.exit(0)

    # Print the posts
    print("")
    print("Found " + str(len(posts_since_cadence)) + " new posts since last check:")
    for post in posts_since_cadence:
        print(post["title"])

    return True


if __name__ == "__main__":
    main()
