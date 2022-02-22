import pytest
import requests
import json
import logging
import random
from utils.utils_posts import CREATE_URL, GOREST_HEADERS, generate_body, get_all_posts, use_existing_post_id, \
    random_string, use_existing_user_id

LOGGER = logging.getLogger(__name__)


@pytest.mark.tc23  # As an authenticated api consumer I can create new user post (POST)
def test_add_new_posts():
    url = CREATE_URL + "posts"

    data_body = generate_body("post")
    payload = json.dumps(data_body)
    logging.info(data_body)

    response = requests.post(url, headers=GOREST_HEADERS, data=payload)
    # logging.info(response.text)

    responseJson = json.loads(response.text)
    # logging.info(responseJson)
    id = responseJson["data"]["id"]
    # logging.info(id)

    assert response.status_code == 201  # created

    response = requests.get(url = (url + '/' + str(id)), headers=GOREST_HEADERS)

    assert response.status_code == 200  # ok


@pytest.mark.tc27  # As an authenticated api consumer I can display all users posts (GET)
def test_get_all_posts():
    number_of_list_elements, number_of_posts = get_all_posts()
    logging.info(number_of_list_elements)
    logging.info(number_of_posts)

    assert number_of_list_elements == number_of_posts


@pytest.mark.tc25  # As an authenticated api consumer I can update already existing post (PATCH)
def test_update_post():
    post_id = use_existing_post_id()
    url = CREATE_URL + "posts" + '/' + str(post_id)
    response = requests.get(url, headers=GOREST_HEADERS)

    responseJson = json.loads(response.text)
    id = responseJson["data"]["id"]

    x = random_string(20)
    payload = json.dumps({"title": x})
    logging.info(x)
    response = requests.patch(url, headers=GOREST_HEADERS, data=payload)

    response = requests.get(url, headers=GOREST_HEADERS)
    responseJson = json.loads(response.text)
    logging.info(responseJson["data"]["title"])

    assert response.status_code == 200
    assert x == responseJson["data"]["title"]


@pytest.mark.tc29  # As an authenticated api consumer I can delete user post (DELETE)
def test_delete_post():
    url = CREATE_URL + "posts"

    POST_DICT = generate_body("post")
    payload = json.dumps(POST_DICT)
    response = requests.post(url, headers=GOREST_HEADERS, data=payload)
    logging.info(response.text)

    assert response.status_code == 201

    responseJson = json.loads(response.text)
    # logging.info(responseJson)
    id = responseJson["data"]["id"]
    logging.info(id)

    delete_url = CREATE_URL + "posts/" + str(id)
    response = requests.delete(delete_url, headers=GOREST_HEADERS)

    assert response.status_code == 204  # no content


@pytest.mark.tc46  # As an authenticated api consumer I can update already existing post (PUT)
def test_put_post():
    post_id = use_existing_post_id()
    url = CREATE_URL + "posts" + '/' + str(post_id)
    response = requests.get(url, headers=GOREST_HEADERS)

    responseJson = json.loads(response.text)
    id = responseJson["data"]["id"]

    POST_DICT = generate_body("post")
    payload = json.dumps(POST_DICT)
    logging.info(payload)

    response = requests.put(url, headers=GOREST_HEADERS, data=payload)

    assert response.status_code == 200

    response = requests.get(url, headers=GOREST_HEADERS)
    responseJson = json.loads(response.text)
    logging.info(response.text)

    assert response.status_code == 200

    assert POST_DICT["user_id"] == responseJson["data"]["user_id"]
    assert POST_DICT["title"] == responseJson["data"]["title"]
    assert POST_DICT["body"] == responseJson["data"]["body"]


@pytest.mark.tc11  # As an anonymous api consumer I can get a given page of users (GET)
def test_get_first_page_of_users():
    GOREST_HEADERS = {'Content-Type': 'application/json'}
    url = CREATE_URL + "users"
    response = requests.get(url, headers=GOREST_HEADERS)
    responseJson = json.loads(response.text)

    number_of_pages = responseJson["meta"]["pagination"]["pages"]
    # logging.info(f"Pages: {number_of_pages}")

    selected_page = random.randint(1, number_of_pages)
    # logging.info(selected_page)
    url = CREATE_URL + "users" + f"?page={selected_page}"
    # logging.info(url)

    response = requests.get(url, headers=GOREST_HEADERS)
    logging.info(response.text)

    assert response.status_code == 200


@pytest.mark.tc14  # As an anonymous api consumer I cannot delete a given user (DELETE)
def test_cannot_delete_user():
    HEADERS = {'Content-Type': 'application/json'}
    user_id = use_existing_user_id()
    url = CREATE_URL + "users" + '/' + str(user_id)

    response = requests.get(url, headers=HEADERS)
    # logging.info(response.text)
    responseJson = json.loads(response.text)
    id = responseJson["data"]["id"]
    # logging.info(id)

    assert response.status_code == 200

    delete_url = CREATE_URL + "users/" + str(id)
    response = requests.delete(delete_url, headers=HEADERS)

    assert response.status_code == 401 # authentication failed
    logging.info(f"Response status_code is {response.status_code} -> authentication failed")


@pytest.mark.tc100  # function needed for integration testing
def test_create_new_user():
    url = CREATE_URL + "users"
    data_body = generate_body("user")
    # logging.info(f"Generate user body -> {data_body}")
    payload = json.dumps(data_body)

    response = requests.post(url, headers=GOREST_HEADERS, data=payload)
    logging.info(f"Response text - create new user -> {response.text}")

    assert response.status_code == 201  # created

    responseJson = json.loads(response.text)
    user_id = responseJson["data"]["id"]
    logging.info(f"User id -> {user_id}")

    return user_id


@pytest.mark.tc101  # function needed for integration testing
def test_create_new_user_post():
    user_id = test_create_new_user()

    data_body = generate_body("post")
    data_body["user_id"] = user_id
    # logging.info(f"Generate post body -> {data_body}")
    payload = json.dumps(data_body)

    url = CREATE_URL + "posts"
    response = requests.post(url, headers=GOREST_HEADERS, data=payload)
    logging.info(f"Response text - create new user post -> {response.text}")

    responseJson = json.loads(response.text)
    post_id = responseJson["data"]["id"]
    user_id = responseJson["data"]["user_id"]
    # logging.info(f"Post id -> {post_id}")
    logging.info(f"User id -> {user_id}")

    url = CREATE_URL + "posts" + '/' + str(post_id)
    response = requests.get(url, headers=GOREST_HEADERS)
    logging.info(f"Get created post {response.text}")

    assert response.status_code == 200  # ok

    return user_id


@pytest.mark.tc102  # function needed for integration testing
def test_delete_created_user(user_id=None):
    # user_id = test_create_new_user()
    if not user_id:
        user_id = test_create_new_user()

    delete_url = CREATE_URL + "users" + "/" + str(user_id)
    logging.info(f"Delete URL {delete_url}")
    response = requests.delete(delete_url, headers=GOREST_HEADERS)
    logging.info(f"Here should be an empty place -> {response.text}")

    assert response.status_code == 204  # no content
