"""Module to handle LinkedIn API calls."""

import json
import logging
import requests
import os


def get_user_id(access_token):
    """
    Get the user ID from LinkedIn.

    Args:
        access_token: The access token to use.

    Returns:
        The user ID.
    """


def create_article(post_detail, access_token):
    """Create an article.

    Args:
        post_detail: The post detail to create the article from.
        access_token: The access token to use.

    Returns:
        True if successful
    """
    logging.info("Creating Linkedin article for %s", post_detail["title"])

    headers = {
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    # Create the article
    article = {
        "author": f"urn:li:person:{get_user_id(access_token)}",
        "lifecycleState": "DRAFT",
        "visibility": "PUBLIC",
        "content": {"contentEntities": [{"entityLocation": post_detail["link"]}]},
    }

    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers=headers,
        data=json.dumps(article),
    )

    print(response.text)

    return True
