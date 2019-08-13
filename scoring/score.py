# -*- coding: utf-8 -*-

import collections


class InvalidScoresheetException(Exception):
    pass


POINTS_HELD = 1
POINTS_GROUND = 2
POINTS_PLATFORM = 5

NUM_TOKENS_IN_ARENA = 16


class Scorer(object):
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

        for info in self._teams_data.values():
            info.setdefault('tokens_held', 0)

        for info in self._arena_data.values():
            info.setdefault('tokens_ground', 0)
            info.setdefault('tokens_platform', 0)

    def validate(self, extra):
        token_counts = (
            [x['tokens_held'] for x in self._teams_data.values()] +
            [extra.get('tokens_ground', 0)] +
            [x['tokens_ground'] for x in self._arena_data.values()] +
            [x['tokens_platform'] for x in self._arena_data.values()]
        )

        negative_counts = [x for x in token_counts if x < 0]
        if negative_counts:
            raise InvalidScoresheetException(
                "Negative token counts are not valid (got {})".format(
                    " and ".join(str(x) for x in negative_counts),
                ),
            )

        num_tokens = sum(token_counts)
        if num_tokens != NUM_TOKENS_IN_ARENA:
            raise InvalidScoresheetException(
                "Wrong number of tokens: {} ≠ {}".format(
                    num_tokens,
                    NUM_TOKENS_IN_ARENA,
                ),
            )

    def calculate_scores(self):
        scores_by_zone = {
            zone: info['tokens_ground'] * POINTS_GROUND +
                info['tokens_platform'] * POINTS_PLATFORM
            for zone, info in self._arena_data.items()
        }

        scores_by_tla = {
            tla: info['tokens_held'] * POINTS_HELD
            for tla, info in self._teams_data.items()
        }

        scores = {
            tla: scores_by_zone[info['zone']] + scores_by_tla[tla]
            for tla, info in self._teams_data.items()
        }
        return scores


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
