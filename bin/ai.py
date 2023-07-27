"""Module for speaking with Google Bard API.

This is temporarily using the bardapi package from PyPI. This will be replaced when the API is made public.
"""

import bardapi
import logging
import time
import os
import sys

from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("BARD_TOKEN")


def get_summary(input_text):
    """
    Get the summary from the API.

    Args:
        input_text: The text to summarize.

    Returns:
        The summary.
    """
    while True:
        # Send an API request and get a response.
        try:
            response = bardapi.core.Bard(token).get_answer(
                "Summarise the following html, write your response as the author of the article. Use first person  : "
                + input_text
            )["content"]
        except Exception as error_message:
            raise Exception(str(error_message)) from error_message

        # Check for text "Unable to get response" in the response.
        if "Unable to get response" in response:
            logging.info("Unable to get response. Trying again...")
            time.sleep(10)
            continue
        else:
            break

    return response
