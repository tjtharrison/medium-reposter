import os
import requests

from dotenv import load_dotenv
load_dotenv()

headers = {
    'Authorization': 'Bearer ' + os.environ.get("LINKEDIN_AUTH_TOKEN"),
    'Connection': 'Keep-Alive',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data_auth = {
    'token': os.environ.get("LINKEDIN_AUTH_TOKEN"),
    'client_id': os.environ.get("LINKEDIN_CLIENT_ID"),
    'client_secret': os.environ.get("LINKEDIN_CLIENT_SECRET"),
}

def validate_token():
    """
    Validate the provided token.

    Returns:
        True if the token is valid, False otherwise.
    """

    response = requests.post(
        'https://www.linkedin.com/oauth/v2/introspectToken',
        headers=headers,
        data=data_auth
    )

    if response.status_code == 200 and response.json()['active']:
        return True

def get_user_info():
    """
    Get the user info.

    Returns:
        The user info.
    """

    response = requests.get(
        'https://api.linkedin.com/v2/me',
        headers=headers,
        data=data_auth
    )

    print(response.text)

    if response.status_code == 200:
        return response.json()

# def post_article():
#     """
#     Post an article on LinkedIn.
#
#     Returns:
#         True if the article was posted successfully, False otherwise.
#     """
#     response = requests.post(
#         'https://api.linkedin.com/v2/ugcPosts',
#         headers=headers,
#         data=data
#     )
#
#     # {
#     #     'author': 'urn:li:person:<your_linkedin_id>',
#     #     'lifecycleState': 'PUBLISHED',
#     #     'specificContent': {
#     #         'com.linkedin.ugc.ShareContent': {
#     #             'shareCommentary': {
#     #                 'text': 'Check out our latest blog post!',
#     #             },
#     #             'shareMediaCategory': 'ARTICLE',
#     #             'media': [
#     #                 {
#     #                     'status': 'READY',
#     #                     'description': {
#     #                         'text': 'Read our latest blog post about LinkedIn API!',
#     #                     },
#     #                     'originalUrl': '<your_blog_post_url>',
#     #                 },
#     #             ],
#     #         },
#     #     },
#     #     'visibility': {
#     #         'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
#     #     },
#     # }
#
#     print(response.text)
#
#     if response.status_code == 201:
#         return True

def main():
    """Main function."""

    if validate_token():
        print('Token is valid')

        user_info = get_user_info()
        print(user_info)



if __name__ == '__main__':
    main()