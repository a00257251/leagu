import flask
import flask_restful
import unittest
import requests


class TestFlaskApiUsingRequests(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get('http://127.0.0.1:5000/rest/KK/2773')
        self.assertEqual(response.json(),[{u'Id': 2773,
  u'away': u'Southampton',
  u'home': u'Arsenal'}])

    def test_main_page(self):
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(response.status_code, 200)

    def test_results_page(self):
        response = requests.get('http://127.0.0.1:5000/view')
        self.assertEqual(response.status_code, 200)

    def test_team_page(self):
        response = requests.get('http://127.0.0.1:5000/team')
        self.assertEqual(response.status_code, 200)

    def test_MatchResults_page(self):
        response = requests.get('http://127.0.0.1:5000/MatchesResult')
        self.assertEqual(response.status_code, 200)

    def testFixtures_page(self):
        response = requests.get('http://127.0.0.1:5000/Fixtures')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()