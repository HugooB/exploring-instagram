from instagram.client import InstagramAPI


def get_tokens():
    file = open("tokens.txt", "r")
    access_token = file.readline().strip()
    client_secret = file.readline().strip()
    user_id = file.readline().strip()
    return access_token, client_secret, user_id


def get_user_info(user_id):
    user = api.user(user_id)
    username = user.username
    full_name = user.full_name
    bio = user.bio
    website = user.website
    key, count_media = user.counts.popitem()
    key, count_follows = user.counts.popitem()
    key, count_followed_by = user.counts.popitem()
    print count_media
    print count_follows
    print count_followed_by


if __name__ == '__main__':
    print "Started!"

    # First set tokens for authentication with API
    access_token, client_secret, user_id = get_tokens()
    api = InstagramAPI(access_token=access_token, client_secret=client_secret)

    # Get the user information
    get_user_info(user_id)

    recent_media, next_ = api.user_recent_media(user_id=user_id, count=334)
    for media in recent_media:
        print media.caption.text