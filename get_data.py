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
    _, count_media = user.counts.popitem()
    _, count_follows = user.counts.popitem()
    _, count_followed_by = user.counts.popitem()
    return user, username, full_name, bio, website, count_media, count_follows, count_followed_by


if __name__ == '__main__':
    print "Started!"

    # First set tokens for authentication with API
    access_token, client_secret, user_id = get_tokens()
    api = InstagramAPI(access_token=access_token, client_secret=client_secret)

    # Get the user information
    user, username, full_name, bio, website, count_media, count_follows, count_followed_by = get_user_info(user_id)

    # Get most recent media
    recent_media, next_ = api.user_recent_media(user_id=user_id, count=30)
    for media in recent_media:
        likes = media.like_count
        comments = media.comment_count
        caption = media.caption.text
        type = media.type
        users_in_photo = len(media.users_in_photo)
        creation_time = media.created_time
        # location_latitude = media.location // not working..
        tags = media.tags
        link = media.link
        filter = media.filter
        image_url = media.get_standard_resolution_url()

    # Get this in a table!

