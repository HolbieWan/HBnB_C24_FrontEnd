import unittest
from app.tests.tests_models import test_user_class
from app.tests.tests_models import test_place_class
from app.tests.tests_models import test_amenity_class
from app.tests.tests_models import test_review_class

from app.tests.tests_repository import test_memory_repo
from app.tests.tests_repository import test_SQLalchemy_repo

from app.tests.tests_facade import test_facade

from app.tests.tests_endpoints.test_login_endpoints import TestAuthEndpoints
from app.tests.tests_endpoints.test_user_endpoints import TestUserEndpoints
from app.tests.tests_endpoints.test_place_endpoints import TestPlaceEndpoints
from app.tests.tests_endpoints.test_amenity_endpoints import TestAmenityEndpoints
from app.tests.tests_endpoints.test_review_endpoints import TestReviewEndpoints


if __name__ == '__main__':
    unittest.main()