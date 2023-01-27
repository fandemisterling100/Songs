import datetime
import logging
from decimal import Decimal
import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from app.api.random_number import RandomNumberConnector
from app.api.models import Song

User = get_user_model()

class TestUserRegisterValidations(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_valid_email_address(self):
        """
        1.a. Test register with valid email adress
        """
        url = reverse("api:register")
        response = self.client.post(
            url, data={"email": "harrypotter", "password": "testpassWR!1"}
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("email" in response_json)
        self.assertTrue(response_json["email"][0] == 'Enter a valid email address.')
        
    def test_existing_email(self):
        """
        1.b. Test attempt to register existing email in database
        """
        url = reverse("api:register")
        email = "harrypotter@hotmail.com"
        password = "testpassWR!1"
        for _ in range(2):
            response = self.client.post(
                url, data={"email": email, "password": password}
            )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("email" in response_json)
        self.assertTrue(response_json["email"][0] == f"The email '{email}' is not available.")
        
    def test_valid_password(self):
        """
        1.c. Password must contain at least 10 characters, one lowercase
        letter, one uppercase letter, and on of the following characters:
        !, @, #, ? or ]
        """
        url = reverse("api:register")
        email = "harrypotter@hotmail.com"
        password_options = ("123", "1234507890", "1234507890A", "1234507890Am")
        validation_messages = (
            'Password must be at least 10 characters long',
            'Password must have at least one uppercase letter',
            'Password must have at least one lowercase letter',
            'The password must contain at least one of the following characters: !, @, #, ? or ]',
        ) 
        for i in range(len(password_options)):
            password = password_options[i]
            message = validation_messages[i]
            response = self.client.post(
                url, data={"email": email, "password": password}
            )
            response_json = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue("password" in response_json)
            self.assertTrue(response_json["password"][0] == message)
            
        password = "1234507890Am!"
        response = self.client.post(
            url, data={"email": email, "password": password}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_valid_register(self):
        """
        Test user register through API
        """
        url = reverse("api:register")
        response = self.client.post(
            url, data={"email": "harrypotter@hotmail.com", "password": "testpassWR!1"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
    
class TestUserLoginValidations(APITestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse("api:register")
        self.client.post(
            url, data={"email": "harrypotter@hotmail.com", "password": "testpassWR!1"}
        )
        
    def test_valid_email_address(self):
        """
        2.a. Test attempt to login with an invalid email
        """
        email = "harrypotter"
        password = "testpassWR!1"
        url = reverse("api:token_obtain_pair")
        response = self.client.post(
            url, data={"email": email, "password": password}
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("email" in response_json)
        self.assertTrue(response_json["email"][0] == 'Enter a valid email address.')
        
    def test_valid_password(self):
        """
        2.c. Password must contain at least 10 characters, one lowercase
        letter, one uppercase letter, and on of the following characters:
        !, @, #, ? or ]
        """
        email = "harrypotter"
        url = reverse("api:token_obtain_pair")
        password_options = ("123", "1234507890", "1234507890A", "1234507890Am")
        validation_messages = (
            'Password must be at least 10 characters long',
            'Password must have at least one uppercase letter',
            'Password must have at least one lowercase letter',
            'The password must contain at least one of the following characters: !, @, #, ? or ]',
        ) 
        for i in range(len(password_options)):
            password = password_options[i]
            message = validation_messages[i]
            response = self.client.post(
                url, data={"email": email, "password": password}
            )
            response_json = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertTrue("password" in response_json)
            self.assertTrue(response_json["password"][0] == message)


class TestUserAuthorization(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_unauthorized(self):
        """
        Test get songs without authorization token
        """
        url = reverse("api:register")
        self.client.post(
            url, data={"email": "harrypotter@hotmail.com", "password": "testpassWR!1"}
        )
        url = reverse("api:retrieve_all_songs")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_authorized(self):
        """
        Test of obtaining access token and refresh. 
        Test of access to an endpoint using the authorization token
        """
        url = reverse("api:register")
        self.client.post(
            url, data={"email": "harrypotter@hotmail.com", "password": "testpassWR!1"}
        )
        url = reverse("api:token_obtain_pair")
        response = self.client.post(
            url, data={"email": "harrypotter@hotmail.com", "password": "testpassWR!1"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertTrue("access" in response_json)
        self.assertTrue("refresh" in response_json)
        
        url = reverse("api:retrieve_all_songs")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response_json.get("access"))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class TestSongViews(APITestCase):
    def setUp(self):
        self.client = APIClient()
        url = reverse("api:register")
        test_password = "testpassWR!1"

        # User 1
        self.email_user_1 = "harrypotter@hotmail.com"
        self.client.post(
            url, data={"email": self.email_user_1, "password": test_password}
        )
        self.user_1 = User.objects.get(email=self.email_user_1)
        
        # User 2
        self.email_user_2 = "ronweasley@hotmail.com"
        self.client.post(
            url, data={"email": self.email_user_2, "password": test_password}
        )
        self.user_2 = User.objects.get(email=self.email_user_2)
        
        # Access token User 1
        response = self.client.post(
            reverse("api:token_obtain_pair"), data={"email": self.email_user_1, "password": test_password}
        )
        response_json = response.json()
        self.access_token_user_1 = response_json.get("access")
        
        # Access token User 2
        response = self.client.post(
            reverse("api:token_obtain_pair"), data={"email": self.email_user_2, "password": test_password}
        )
        response_json = response.json()
        self.access_token_user_2 = response_json.get("access")
        
    def test_create_songs(self):
        """
        3.a Test of songs creation (private and public)
        """
        url = reverse("api:create_song")
        private_song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "true",
        }
        public_song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "false",
        }
        initial_private_songs = Song.objects.filter(private=True).count()
        initial_public_songs = Song.objects.filter(private=False).count()
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        response_public = self.client.post(
            url, data=public_song, format='json'
        )
        self.assertEqual(response_public.status_code, status.HTTP_201_CREATED)
        self.assertTrue("Song created" in response_public.data)
        response_private = self.client.post(
            url, data=private_song, format='json'
        )
        self.assertEqual(response_private.status_code, status.HTTP_201_CREATED)
        self.assertTrue("Song created" in response_public.data)
        
        self.assertEqual(Song.objects.filter(private=False).count(), initial_public_songs + 1)
        self.assertEqual(Song.objects.filter(private=True).count(), initial_private_songs + 1)
        
        
    def test_read_songs(self):
        """
        3.b Test for obtaining songs created by the user who requests them
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        url_create = reverse("api:create_song")
        url_read = reverse("api:retrieve_all_songs")
        song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "true",
        }
        response = self.client.get(url_read)
        
        # Get total songs from the paginator metadata
        initial_songs = response.json()["meta"]["total_results"]
        self.client.post(
            url_create, data=song, format='json'
        )
        response = self.client.get(url_read)
        final_songs = response.json()["meta"]["total_results"]
        
        self.assertEqual(final_songs, initial_songs + 1)
        
    def test_valid_song_update(self):
        """
        3.c Test to update an own song and a song from another user
        """
        
        url_create = reverse("api:create_song")
        song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "true",
        }
        updated_song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "false",
        }
        
        # User 1 creates a song
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        response = self.client.post(
            url_create, data=song, format='json'
        )
        response_json = response.json()
        song_id = response_json["Song created"]["pk"]
        song_user_1 = Song.objects.get(pk=song_id)
        
        # User 1 tries to update a song of its own
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        url_update = reverse("api:update_song", kwargs={'pk': song_user_1.pk})
        response = self.client.put(
            url_update, data=updated_song, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # User 2 creates a song
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_2)
        response = self.client.post(
            url_create, data=song, format='json'
        )
        response_json = response.json()
        song_id = response_json["Song created"]["pk"]
        song_user_2 = Song.objects.get(pk=song_id)
        
        # User 1 tries to update the song created by User 2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        url_update = reverse("api:update_song", kwargs={'pk': song_user_2.pk})
        response = self.client.put(
            url_update, data=updated_song, format='json'
        )
        
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Permission denied' in response_json)
        self.assertEqual(response_json['Permission denied'], 'This song is private, you can not update it.')
        
    def test_valid_song_reading(self):
        """
        Test to read a song by id created by the requesting user,
        a song by id created by another user, list all songs 
        created by the authorized user and list all public songs
        """
        
        url_create = reverse("api:create_song")
        song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "true",
        }
        initial_user_1_songs = Song.objects.filter(created_by=self.user_1).count()
        
        # User 1 creates a song
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        response = self.client.post(
            url_create, data=song, format='json'
        )
        response_json = response.json()
        song_id = response_json["Song created"]["pk"]
        song_user_1 = Song.objects.get(pk=song_id)
        
        # Get all songs (created by User 1)
        url_get = reverse("api:retrieve_all_songs")
        response = self.client.get(url_get)
        self.assertEqual(response.json()["meta"]["total_results"], initial_user_1_songs + 1)
        
        # Get all public songs
        url_get = reverse("api:retrieve_all_public_songs")
        public_songs = Song.objects.filter(private=False).count()
        response = self.client.get(url_get)
        self.assertEqual(response.json()["meta"]["total_results"], public_songs)
        
        # Try to read a song created by User 1
        url_get = reverse("api:retrieve_song", kwargs={'pk': song_user_1.pk})
        response = self.client.get(url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # User 2 creates a private song
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_2)
        response = self.client.post(
            url_create, data=song, format='json'
        )
        response_json = response.json()
        song_id = response_json["Song created"]["pk"]
        song_user_2 = Song.objects.get(pk=song_id)
        
        # Try to read a private song created by other user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        url_get = reverse("api:retrieve_song", kwargs={'pk': song_user_2.pk})
        response = self.client.get(url_get)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Permission denied' in response_json)
        self.assertEqual(response_json['Permission denied'], 'This song is private, you can not retrieve it.')
        
        # User 2 creates a public song
        song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "false",
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_2)
        response = self.client.post(
            url_create, data=song, format='json'
        )
        response_json = response.json()
        song_id = response_json["Song created"]["pk"]
        song_user_2 = Song.objects.get(pk=song_id)
        
        # Try to read a public song created by other user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        url_get = reverse("api:retrieve_song", kwargs={'pk': song_user_2.pk})
        response = self.client.get(url_get)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_song(self):
        """
        Test to delete a song created by the authorized
        user and a song created by another user
        """
        
        url_create = reverse("api:create_song")
        song = {
            "name": "Satellite",
            "artist": "Khalid",
            "album": "Satellite",
            "duration": "00:03:07",
            "favorite": "true",
            "private": "true",
        }
        
        # User 1 creates a song
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        response = self.client.post(
            url_create, data=song, format='json'
        )
        response_json = response.json()
        song_id = response_json["Song created"]["pk"]
        song_user_1 = Song.objects.get(pk=song_id)
        
        # User 1 deletes its own song
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        url_delete = reverse("api:delete_song", kwargs={'pk': song_user_1.pk})
        response = self.client.delete(url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # User 2 creates a song
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_2)
        response = self.client.post(
            url_create, data=song, format='json'
        )
        response_json = response.json()
        song_id = response_json["Song created"]["pk"]
        song_user_2 = Song.objects.get(pk=song_id)
        
        # User 1 tries to delete the song created by User 2
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_user_1)
        url_delete = reverse("api:delete_song", kwargs={'pk': song_user_2.pk})
        response = self.client.delete(url_delete)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Permission denied' in response_json)
        self.assertEqual(response_json['Permission denied'], 'This song is private, you can not delete it.')
    
    
class TestRandomNumberConnector(APITestCase):
    """
    Test connector to get random number from public API
    """
    def test_get_random_number(self):
        connector = RandomNumberConnector()
        random_number = connector.get_number()
        self.assertTrue(isinstance(random_number, int))
        