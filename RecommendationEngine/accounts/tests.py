from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import CustomUser

import os
import sqlite3
import RecommendationEngine.placeholder_db

class AccountsTests(TestCase):
    def test_signup_view(self):
        url = reverse('signup') # This is the /api/signup endpoint

        # Data to post into the sinup form
        data = {
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }

        #Creating the post and calling data and url into it
        response = self.client.post(url, data)

        #Checking whether the response code is 302 (Redirect to accounts/login/)
        self.assertEqual(response.status_code, 302)
        print(response.status_code)
        print(response.headers['Location'])

        # Checking whether the user was created in the DB
        try:
            user = get_user_model().objects.get(username='testuser')
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'testuser@email.com')
        except get_user_model().DoesNotExist:
            self.fail("User was not created")

    # def DBSetUp(self):
    #     # path:
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #     DB_PATH = os.path.join(BASE_DIR, 'placeholder.db')
        
    #     #connecting to the db
    #     con = sqlite3.connect(DB_PATH)
    #     cur = con.cursor()

    #     #Checking if the table exists
    #     cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #     existing_tables = cur.fetchall()

    #     #List of expected tables
    #     expected_tables = ['USERS', 'DEVS', 'GAMES', 'NEWS']

    #     # Check for the existence of all expected tables
    #     missing_tables = [table for table in expected_tables if (table,) not in existing_tables]

    #     if missing_tables:
    #         # If any tables are missing, create them
    #         for table in missing_tables:
    #             if table == 'USERS':
    #                 # Create the USERS table
    #                 self.create_users_table(cur)
    #             elif table == 'DEVS':
    #                 # Create the DEVS table
    #                 self.create_devs_table(cur)
    #             elif table == 'GAMES':
    #                 # Create the GAMES table
    #                 self.create_games_table(cur)
    #             elif table == 'NEWS':
    #                 # Create the NEWS table
    #                 self.create_news_table(cur)

    #         con.commit()

    #     con.close

    # def test_get_devs(self):
    #     """Test that fetching developers returns a valid JSON response"""
    #     response = self.client.get(reverse('get_devs'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('developers', response.json())

    # def test_add_dev(self):
    #     response = self.client.get(reverse('get_devs'))
    #     self.assertEqual(response.status_code, 200)
    #     json_response = response.json()
    #     self.assertIn('developers', json_response)
    #     self.assertIsInstance(json_response['developers'], list)

    #     # Verify that the developer was added to the database
    #     con, cur = placeholder_db.makeConnection("placeholder.db")
    #     devs = placeholder_db.fetchAllDevelopers(cur)
    #     con.close()
    #     self.assertIn(('New Developer',), devs)