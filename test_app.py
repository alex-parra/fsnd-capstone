import os
import unittest
from app import create_app
from app.models import setup_db, Movie, Actor
from app.config import BASE_URL, AUTH_DOMAIN, AUTH_CLIENT_ID, AUTH_AUDIENCE, TESTING_JWT_KEY
from flask_sqlalchemy import SQLAlchemy
from jose import jwt

test_users = {
    'ep': {'permissions': ['movies:list', 'movies:create', 'movies:update', 'movies:delete', 'actors:list', 'actors:create', 'actors:update', 'actors:delete']},
    'cd': {'permissions': ['movies:list', 'movies:update', 'actors:list', 'actors:create', 'actors:update', 'actors:delete']},
    'ca': {'permissions': ['movies:list', 'actors:list']},
}


def bearer(user):
    token = jwt.encode(test_users[user], TESTING_JWT_KEY)
    return f'Bearer {token}'


class CapstoneTestCase(unittest.TestCase):
    '''This class represents the app test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        with self.app.app_context():  # binds the app to the current context
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        '''Executed after each test'''
        pass

    def test_get_health(self):
        '''Test get_health '''
        res = self.client().get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["status"], "Healthy")
        self.assertIsInstance(res.json["movies"], int)

# ---------------------------------------
# User

    def test_get_user_anon(self):
        '''Test get_user un-authenticated '''
        res = self.client().get("/user")
        self.assertEqual(res.status_code, 401)
        self.assertIsInstance(res.json["error"], int)
        self.assertIsInstance(res.json["message"], str)

    def test_get_user_as_ep(self):
        '''Test get_user as Executive Producer '''
        res = self.client().get(
            "/user", headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["permissions"], list)

    def test_get_user_as_cd(self):
        '''Test get_user as Casting Director '''
        res = self.client().get(
            "/user", headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["permissions"], list)

    def test_get_user_as_ca(self):
        '''Test get_user as Casting Assistant '''
        res = self.client().get(
            "/user", headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["permissions"], list)

# ---------------------------------------
# Movies

    def test_get_movies_anon(self):
        '''Test get_movies un-authenticated '''
        res = self.client().get("/movies")
        self.assertEqual(res.status_code, 401)
        self.assertIsInstance(res.json["error"], int)
        self.assertIsInstance(res.json["message"], str)

    def test_get_movies_as_ep(self):
        '''Test get_movies as Executive Producer '''
        res = self.client().get(
            "/movies", headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movies"], list)

    def test_get_movies_as_cd(self):
        '''Test get_movies as Casting Director '''
        res = self.client().get(
            "/movies", headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movies"], list)

    def test_get_movies_as_ca(self):
        '''Test get_movies as Casting Assistant '''
        res = self.client().get(
            "/movies", headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movies"], list)

    def test_post_movies_anon(self):
        '''Test post_movies un-authenticated '''
        res = self.client().post("/movies")
        self.assertEqual(res.status_code, 401)
        self.assertIsInstance(res.json["error"], int)
        self.assertIsInstance(res.json["message"], str)

    def test_post_movies_ep(self):
        '''Test post_movies as Executive Producer '''
        res = self.client().post(
            "/movies", json={'title': 'Test Movie', 'release_date': '2020-01-15'}, headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movie"], dict)
        movie = Movie.query.get(res.json['movie']['id'])
        movie.delete()

    def test_post_movies_cd(self):
        '''Test post_movies as Casting Director '''
        res = self.client().post(
            "/movies", json={'title': 'Test Movie', 'release_date': '2020-01-15'}, headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 401)

    def test_post_movies_ca(self):
        '''Test post_movies as Casting Assistant '''
        res = self.client().post(
            "/movies", json={'title': 'Test Movie', 'release_date': '2020-01-15'}, headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 401)

    def test_patch_movies_ep(self):
        '''Test patch_movies as Executive Producer '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        res = self.client().patch(
            f'/movies/{movie.id}', json={'title': 'Test Movieeee', 'release_date': '1920-01-15'}, headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movie"], dict)
        movie = Movie.query.get(movie.id)
        self.assertEqual(movie.title, 'Test Movieeee')
        self.assertEqual(movie.release_date, '1920-01-15')
        movie.delete()

    def test_patch_movies_cd(self):
        '''Test patch_movies as Casting Director '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        res = self.client().patch(
            f'/movies/{movie.id}', json={'title': 'Test Movieeee', 'release_date': '1920-01-15'}, headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json['movie'], dict)
        movie = Movie.query.get(movie.id)
        self.assertEqual(movie.title, 'Test Movieeee')
        self.assertEqual(movie.release_date, '1920-01-15')
        movie.delete()

    def test_patch_movies_ca(self):
        '''Test patch_movies as Casting Assistant '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        res = self.client().patch(
            f'/movies/{movie.id}', json={'title': 'Test Movie', 'release_date': '2020-01-15'}, headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 401)
        movie.delete()

    def test_patch_movies_404(self):
        '''Test patch_movies as Executive Producer '''
        res = self.client().patch('/movies/99999999',
                                  json={'title': 'Test Movieeee', 'release_date': '1920-01-15'}, headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 404)

    def test_delete_movies_ep(self):
        '''Test delete_movies as Executive Producer '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        res = self.client().delete(
            f'/movies/{movie.id}', headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json['deleted'], dict)
        self.assertEqual(res.json['deleted']['id'], movie.id)

    def test_delete_movies_cd(self):
        '''Test delete_movies as Casting Director '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        res = self.client().delete(
            f'/movies/{movie.id}', headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 401)
        movie.delete()

    def test_delete_movies_ca(self):
        '''Test delete_movies as Casting Assistant '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        res = self.client().delete(
            f'/movies/{movie.id}', headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 401)
        movie.delete()

# ---------------------------------------
# Actors

    def test_get_actors_anon(self):
        '''Test get_actors un-authenticated '''
        res = self.client().get("/actors")
        self.assertEqual(res.status_code, 401)
        self.assertIsInstance(res.json["error"], int)
        self.assertIsInstance(res.json["message"], str)

    def test_get_actors_as_ep(self):
        '''Test get_actors as Executive Producer '''
        res = self.client().get(
            "/actors", headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["actors"], list)

    def test_get_actors_as_cd(self):
        '''Test get_actors as Casting Director '''
        res = self.client().get(
            "/actors", headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["actors"], list)

    def test_get_actors_as_ca(self):
        '''Test get_actors as Casting Assistant '''
        res = self.client().get(
            "/actors", headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["actors"], list)

    def test_post_actors_anon(self):
        '''Test post_actors un-authenticated '''
        res = self.client().post("/actors")
        self.assertEqual(res.status_code, 401)
        self.assertIsInstance(res.json["error"], int)
        self.assertIsInstance(res.json["message"], str)

    def test_post_actors_ep(self):
        '''Test post_actors as Executive Producer '''
        res = self.client().post(
            "/actors", json={'name': 'Test Actor', 'age': 40, 'gender': 'M'}, headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["actor"], dict)
        actor = Actor.query.get(res.json['actor']['id'])
        actor.delete()

    def test_post_actors_cd(self):
        '''Test post_actors as Casting Director '''
        res = self.client().post(
            "/actors", json={'name': 'Test Actor', 'age': 40, 'gender': 'M'}, headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["actor"], dict)
        actor = Actor.query.get(res.json['actor']['id'])
        actor.delete()

    def test_post_actors_ca(self):
        '''Test post_actors as Casting Assistant '''
        res = self.client().post(
            "/actors", json={'name': 'Test Actor', 'age': 40, 'gender': 'M'}, headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 401)

    def test_patch_actors_ep(self):
        '''Test patch_actors as Executive Producer '''
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().patch(
            f'/actors/{actor.id}', json={'name': 'Test Actorrrr', 'age': 45, 'gender': 'F'}, headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["actor"], dict)
        actor = Actor.query.get(actor.id)
        self.assertEqual(actor.name, 'Test Actorrrr')
        self.assertEqual(actor.age, 45)
        self.assertEqual(actor.gender, 'F')
        actor.delete()

    def test_patch_actors_cd(self):
        '''Test patch_actors as Casting Director '''
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().patch(
            f'/actors/{actor.id}', json={'name': 'Test Actorrrr', 'age': 45, 'gender': 'F'}, headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["actor"], dict)
        actor = Actor.query.get(actor.id)
        self.assertEqual(actor.name, 'Test Actorrrr')
        self.assertEqual(actor.age, 45)
        self.assertEqual(actor.gender, 'F')
        actor.delete()

    def test_patch_actors_ca(self):
        '''Test patch_actors as Casting Assistant '''
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().patch(
            f'/actors/{actor.id}', json={'name': 'Test Actorrrr', 'age': 45, 'gender': 'F'}, headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 401)
        actor.delete()

    def test_patch_actors_404(self):
        '''Test patch_actors as Executive Producer '''
        res = self.client().patch('/actors/99999',
                                  json={'name': 'Test Actorrrr', 'age': 35, 'gender': 'M'}, headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 404)

    def test_delete_actors_ep(self):
        '''Test delete_actors as Executive Producer '''
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().delete(
            f'/actors/{actor.id}', headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json['deleted'], dict)
        self.assertEqual(res.json['deleted']['id'], actor.id)

    def test_delete_actors_cd(self):
        '''Test delete_actors as Casting Director '''
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().delete(
            f'/actors/{actor.id}', headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json['deleted'], dict)
        self.assertEqual(res.json['deleted']['id'], actor.id)

    def test_delete_actors_ca(self):
        '''Test delete_actors as Casting Assistant '''
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().delete(
            f'/actors/{actor.id}', headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 401)
        actor.delete()

# ---------------------------------------
# Movie Actors

    def test_post_movie_actors_ep(self):
        '''Test post_actors as Executive Producer '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().post(f'/movies/{movie.id}/actors', json={
            'actor': {'id': actor.id}}, headers={'Authorization': bearer('ep')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movie"], dict)
        actor.delete()
        movie.delete()

    def test_post_movie_actors_cd(self):
        '''Test post_actors as Casting Director '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().post(f'/movies/{movie.id}/actors', json={
            'actor': {'id': actor.id}}, headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movie"], dict)
        actor.delete()
        movie.delete()

    def test_post_movie_actors_ca(self):
        '''Test post_actors as Casting Assistant '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        res = self.client().post(f'/movies/{movie.id}/actors', json={
            'actor': {'id': actor.id}}, headers={'Authorization': bearer('ca')})
        self.assertEqual(res.status_code, 401)
        actor.delete()
        movie.delete()

    def test_delete_movie_actors_cd(self):
        '''Test delete_actors as Casting Director '''
        movie = Movie(title='Test Movie', release_date='2020-01-15')
        movie.insert()
        actor = Actor(name='Test Actor', age=40, gender='M')
        actor.insert()
        movie.actors.append(actor)
        movie.update()
        res = self.client().delete(f'/movies/{movie.id}/actors', json={
            'actor': {'id': actor.id}}, headers={'Authorization': bearer('cd')})
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json["movie"], dict)
        movie.delete()
        actor.delete()


if __name__ == "__main__":
    unittest.main()
