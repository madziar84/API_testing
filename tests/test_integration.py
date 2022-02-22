import pytest
import logging
from tests.test_posts import test_create_new_user_post, test_delete_created_user

LOGGER = logging.getLogger(__name__)


@pytest.mark.tc39  # As an authenticated api consumer I can:
                   # 1. Create new user (POST),
                   # 2. Create new user post (POST),
                   # 3. Delete just created user (DELETE)
def test_integration():
    # 1. Create new user (POST) and 2. Create new user post (POST)
    user_id = test_create_new_user_post()

    # 3. Delete just created user (DELETE)
    test_delete_created_user(user_id)

    logging.info(f'Created user with user_id {user_id}')
