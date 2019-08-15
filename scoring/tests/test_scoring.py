#!/usr/bin/env python

import unittest

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException


class ScorerTests(unittest.TestCase):
    longMessage = True

    def construct_scorer(self):
        return Scorer(self.teams_data, self.arena_data)

    def assertScores(self, expected_scores):
        scorer = self.construct_scorer()
        actual_scores = scorer.calculate_scores()

        self.assertEqual(expected_scores, actual_scores, "Wrong scores")

    def setUp(self):
        self.teams_data =  {
            'ABC': {'zone': 0, 'tokens_held': 0},
            'DEF': {'zone': 1, 'tokens_held': 0},
            'GHI': {'zone': 2, 'tokens_held': 0},
        }
        self.arena_data = {
            x: {
              'tokens_platform': 0,
              'tokens_ground': 0,
            } for x in range(4)
        }

    # Wrong number of tokens

    def test_too_many_tokens_held(self):
        # There are a total of 16 tokens

        self.teams_data['ABC']['tokens_held'] = 9
        self.teams_data['DEF']['tokens_held'] = 10

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_too_many_tokens_ground(self):
        # There are a total of 16 tokens

        self.arena_data[0]['tokens_ground'] = 9
        self.arena_data[1]['tokens_ground'] = 10

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_too_many_tokens_platform(self):
        # There are a total of 16 tokens

        self.arena_data[1]['tokens_platform'] = 9
        self.arena_data[2]['tokens_platform'] = 10

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_too_many_tokens_mixed(self):
        # There are a total of 16 tokens

        self.teams_data['ABC']['tokens_held'] = 9
        self.arena_data[0]['tokens_ground'] = 9
        self.arena_data[1]['tokens_platform'] = 9

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_too_few_tokens(self):
        # There are a total of 16 tokens, but we don't require that all are
        # accounted for.

        scorer = self.construct_scorer()
        scorer.validate(None)

    # Negative tokens

    def test_negative_tokens_held(self):
        # There are a total of 16 tokens

        self.teams_data['ABC']['tokens_held'] = -9

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_negative_tokens_ground(self):
        # There are a total of 16 tokens

        self.arena_data[0]['tokens_ground'] = -9

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_negative_tokens_platform(self):
        # There are a total of 16 tokens

        self.arena_data[1]['tokens_platform'] = -9

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    # Fractional tokens

    def test_fractional_tokens_held(self):
        # There are a total of 16 tokens

        self.teams_data['ABC']['tokens_held'] = -0.5

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_fractional_tokens_ground(self):
        # There are a total of 16 tokens

        self.arena_data[0]['tokens_ground'] = -0.5

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    def test_fractional_tokens_platform(self):
        # There are a total of 16 tokens

        self.arena_data[1]['tokens_platform'] = -0.5

        scorer = self.construct_scorer()

        with self.assertRaises(InvalidScoresheetException):
            scorer.validate(None)

    # Scoring logic

    def test_no_tokens_moved(self):
        self.assertScores({
            'ABC': 0,
            'DEF': 0,
            'GHI': 0,
        })

    def test_one_robot_holding_token(self):
        self.teams_data['ABC']['tokens_held'] = 1

        self.assertScores({
            'ABC': 1,
            'DEF': 0,
            'GHI': 0,
        })

    def test_one_ground_token(self):
        self.arena_data[1]['tokens_ground'] = 1

        self.assertScores({
            'ABC': 0,
            'DEF': 2,
            'GHI': 0,
        })

    def test_two_ground_tokens(self):
        self.arena_data[1]['tokens_ground'] = 2

        self.assertScores({
            'ABC': 0,
            'DEF': 4,
            'GHI': 0,
        })

    def test_one_platform_token(self):
        self.arena_data[1]['tokens_platform'] = 1

        self.assertScores({
            'ABC': 0,
            'DEF': 5,
            'GHI': 0,
        })

    def test_two_platform_tokens(self):
        self.arena_data[1]['tokens_platform'] = 2

        self.assertScores({
            'ABC': 0,
            'DEF': 10,
            'GHI': 0,
        })

    def test_one_ground_token_one_platform_token(self):
        self.arena_data[1]['tokens_ground'] = 1
        self.arena_data[1]['tokens_platform'] = 1

        self.assertScores({
            'ABC': 0,
            'DEF': 7,
            'GHI': 0,
        })

    def test_one_ground_token_one_platform_token_different_teams(self):
        self.arena_data[1]['tokens_ground'] = 1
        self.arena_data[0]['tokens_platform'] = 1

        self.assertScores({
            'ABC': 5,
            'DEF': 2,
            'GHI': 0,
        })

    def test_many_moved_tokens(self):
        self.arena_data[0]['tokens_ground'] = 2
        self.arena_data[0]['tokens_platform'] = 1

        self.arena_data[1]['tokens_ground'] = 4
        self.teams_data['DEF']['tokens_held'] = 2

        self.assertScores({
            'ABC': 9,
            'DEF': 10,
            'GHI': 0,
        })


if __name__ == '__main__':
    unittest.main()
