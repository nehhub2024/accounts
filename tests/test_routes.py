"""
Account API Service Test Suite
"""
import os
import logging
from unittest import TestCase
from service import app
from service.models import db, Account, init_db
from service.common import status  # HTTP Status Codes
from tests.factories import AccountFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "sqlite:///test.db"
)

BASE_URL = "/accounts"


class TestAccountService(TestCase):
    """Account Service Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Run before each test"""
        self.client = app.test_client()
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Run after each test"""
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_accounts(self, count):
        """Factory method to create accounts in bulk"""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test Account",
            )
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should call the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    def test_create_account(self):
        """It should Create a new Account"""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL, json=account.serialize(), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["address"], account.address)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["active"], account.active)

    def test_create_account_no_content_type(self):
        """It should not Create an Account with no Content-Type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_account_wrong_content_type(self):
        """It should not Create an Account with wrong Content-Type"""
        response = self.client.post(BASE_URL, data="bad data", content_type="text/plain")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # ---------------------------------------------------------
    # LIST
    # ---------------------------------------------------------
    def test_get_account_list(self):
        """It should Get a list of Accounts"""
        self._create_accounts(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------
    def test_get_account(self):
        """It should Read a single Account"""
        account = self._create_accounts(1)[0]
        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], account.name)

    def test_get_account_not_found(self):
        """It should not Read an Account that is not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------
    def test_update_account(self):
        """It should Update an existing Account"""
        account = AccountFactory()
        response = self.client.post(BASE_URL, json=account.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_account = response.get_json()
        new_account["name"] = "Updated Name"
        response = self.client.put(f"{BASE_URL}/{new_account['id']}", json=new_account)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_account = response.get_json()
        self.assertEqual(updated_account["name"], "Updated Name")

    def test_update_account_not_found(self):
        """It should not Update an Account that does not exist"""
        account = AccountFactory()
        response = self.client.put(f"{BASE_URL}/0", json=account.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def test_delete_account(self):
        """It should Delete an Account"""
        account = self._create_accounts(1)[0]
        response = self.client.delete(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account_not_found_is_idempotent(self):
        """It should return 204 even if the Account does not exist (idempotent)"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # ---------------------------------------------------------
    # SECURITY HEADERS / CORS
    # ---------------------------------------------------------
    def test_security_headers(self):
        """It should return security headers set by Talisman"""
        response = self.client.get("/", environ_overrides={"HTTP_HOST": "localhost"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'self'; object-src 'none'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        for key, value in headers.items():
            self.assertEqual(response.headers.get(key), value)

    def test_cors_security(self):
        """It should return a CORS Access-Control-Allow-Origin header"""
        response = self.client.get("/", environ_overrides={"HTTP_HOST": "localhost"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
