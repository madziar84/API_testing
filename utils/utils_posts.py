import requests
import json
import random
import string


CREATE_URL = "https://gorest.co.in/public/v1/"
GOREST_TOKEN = 'da8e2ff091bf79d8d75b9dfbee574fcb44e203053778f0af358cbc0da5a7f0e7'
GOREST_HEADERS = {'Authorization': f'Bearer {GOREST_TOKEN}',
                  'Content-Type': 'application/json'}
USER_DICT = {
    "name": "",
    "email": "",
    "gender": "",
    "status": ""
    }
POST_DICT = {
        "user_id": 0,
        "title": "",
        "body": ""
    }


def random_string(lenght):
    letters = string.ascii_letters
    random_title = ''.join(random.choice(letters) for i in range(lenght))
    return random_title


def random_email():
    return random_string(5) + '@email.com'


def use_existing_user_id():
    url = CREATE_URL + "users?page=1"
    response = requests.get(url, headers=GOREST_HEADERS)

    responseJson = json.loads(response.text)

    count = len(responseJson["data"])
    random_value = random.randint(0, count-1)
    existing_id = responseJson["data"][random_value]["id"]
    return existing_id


def use_existing_post_id():
    url = CREATE_URL + "posts?page=1"
    response = requests.get(url, headers=GOREST_HEADERS)

    responseJson = json.loads(response.text)

    count = len(responseJson["data"])
    random_value = random.randint(0, count-1)
    existing_id = responseJson["data"][random_value]["id"]
    return existing_id


def generate_body(resource):
    if resource == "user":
        USER_DICT['name'] = random_string(8)
        USER_DICT['email'] = random_email()
        USER_DICT['gender'] = 'male'
        USER_DICT['status'] = 'active'
        data_body = USER_DICT
    elif resource == "post":
        POST_DICT['user_id'] = use_existing_user_id()
        POST_DICT['title'] = random_string(10)
        POST_DICT['body'] = random_string(40)
        data_body = POST_DICT
    return data_body


def get_all_posts():
    url = CREATE_URL + "posts"

    response = requests.get(url, headers=GOREST_HEADERS)

    # we are looking in response 'total:' and 'pages:'
    responseJson = json.loads(response.text)
    # print(type(responseJson))
    number_of_pages = responseJson["meta"]["pagination"]["pages"]
    number_of_posts = responseJson["meta"]["pagination"]["total"]
    # print(number_of_pages, number_of_posts)

    # we make a for loop that will take all post id's from all sides and collect them in a list
    my_list = []
    try:
        for page in range(1, (number_of_pages + 1)):
            url = CREATE_URL + "posts" + f"?page={page}"
            page_response = requests.get(url, headers=GOREST_HEADERS)
            responseJson = json.loads(page_response.text)
            for post in range(0, 20):
                post_id = responseJson["data"][post]["id"]
                # print(post_id)
                my_list.append(post_id)
    except IndexError:
        print("Done")
        # print(my_list)
    number_of_list_elements = len(my_list)
    print(number_of_list_elements, number_of_posts)

    return number_of_list_elements, number_of_posts
