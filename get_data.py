import requests
import json
import os
import emoji
import csv
import pandas as pd
import sys

def get_tokens():
    file = open("tokens.txt", "r")
    access_token = file.readline().strip()
    client_secret = file.readline().strip()
    user_id = file.readline().strip()
    return access_token, client_secret, user_id

def get_user_info(access_token):
    response = json.loads(requests.get("https://api.instagram.com/v1/users/self/?access_token="+ access_token).text)

    if response['meta']['code'] == 200:
        # Parse response text
        user = dict()
        user['id'] = response['data']['id']
        user['username'] = response['data']['username']
        user['full_name'] = response['data']['full_name']
        user['bio'] = response['data']['bio']
        user['website'] = response['data']['website']
        user['count_media'] = response['data']['counts']['media']
        user['count_follows'] = response['data']['counts']['follows']
        user['count_followed_by'] = response['data']['counts']['followed_by']
        return user
    else:
        print("[!] Error", response['meta']['code'], response['meta']['error_type'], response['meta']['error_message'] )

def get_amount_of(text, character):
    if character == "emoji":
        num_of_emoji = 0
        for c in text:
            if c in emoji.UNICODE_EMOJI:
                num_of_emoji += 1
        return num_of_emoji
    else:
        return text.count(character)

def parse_media_object(media):
    # Create new dict to store the object in
    media_item = dict()

    # Parse all information
    media_item['id'] = media['id']
    media_item['likes'] = media['likes']['count']
    media_item['comments'] = media['comments']['count']
    try:
        media_item['caption'] = media['caption']['text']
    except:
        media_item['caption'] = "empty"
    media_item['type'] = media['type']
    media_item['users_in_photo'] = len(media['users_in_photo'])
    media_item['creation_time'] = media['created_time']
    media_item['tags'] = "".join(media['tags'])
    media_item['link'] = media['link']
    media_item['filter'] = media['filter']
    media_item['image_url'] = media['images']['standard_resolution']['url']
    media_item['location'] = 0 if media['location'] == None else 1

    # If location information is available, parse it
    try:
        media_item['location_latitude'] = media['location']['latitude']
        media_item['location_longitude'] = media['location']['longitude']
        media_item['location_name'] = media['location']['name']
    except:
        media_item['location_latitude'] = 0
        media_item['location_longitude'] = 0
        media_item['location_name'] = "unknown"

    # Get the number of hashtags and mentions
    media_item['no_hashtags'] = get_amount_of(media_item['caption'], "#")
    media_item['no_usertags'] = get_amount_of(media_item['caption'],"@")
    media_item['no_emoji'] = get_amount_of(media_item['caption'],"emoji")

    return media_item

def get_recent_media(access_token):
    response = json.loads(requests.get("https://api.instagram.com/v1/users/self/media/recent/?access_token="+ access_token).text)
    recent_media = list()
    if response['meta']['code'] == 200:
        for item in response['data']:
            media_item = parse_media_object(item)
            recent_media.append(media_item)
    return recent_media

def download_image(image, output):
    url = image['image_url']
    r = requests.get(url, allow_redirects=True)
    file_path = os.path.join(output, image['id'] + ".jpg")
    open(file_path, 'wb').write(r.content)

if __name__ == '__main__':
    print("Started!")

    # First set tokens for authentication with API
    access_token, client_secret, user_id = get_tokens()

    # Download the user information
    user = get_user_info(access_token)
    if user == None:
        continue
    print("Successfully got the information of", user['full_name'], "!")

    # Get most recent media
    print("Accessing your latest media")
    recent_media = get_recent_media(access_token)

    # Create folder and store all photos in
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Create a folder for this users
    user_folder = os.path.join("temp", user['id'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Now download all the images from recent media
    print("Downloading your recent images")
    for image in recent_media:
        download_image(image, os.path.join("temp", user['id']))

    # Save the results to a csv file
    pd.DataFrame(recent_media).to_csv(os.path.join(user_folder, 'media_data.csv'))
