import unittest

from live_arbitrage_identificator.utils.load_env import load_db_env, load_oddsportal_env, load_env_variables


class TestLoadENV(unittest.TestCase):
    def test_load_db_env(self):
        expected_keys = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
        db_env = load_db_env()
        self.assertEqual(len(db_env), 5)
        self.assertEqual(list(db_env.keys()), expected_keys)

    def test_load_oddsportal_env(self):
        oddsportal_env = load_oddsportal_env()
        self.assertEqual(len(oddsportal_env), 2)
        self.assertIsNotNone(oddsportal_env[0])
        self.assertIsNotNone(oddsportal_env[1])
