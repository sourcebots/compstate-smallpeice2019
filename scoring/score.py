import itertools
import collections


class InvalidScoresheetException(Exception):
    pass


POINTS_HELD = 1
POINTS_GROUND = 2
POINTS_PLATFORM = 5

NUM_TOKENS = 16


class Scorer(object):
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

    def validate(self, extra):
        num_tokens = sum(itertools.chain(
            [x.get('tokens_held', 0) for x in self._teams_data.values()],
            [extra.get('tokens_ground', 0)],
            [x.get('tokens_ground', 0) for x in self._arena_data.values()],
            [x.get('tokens_platform', 0) for x in self._arena_data.values()],
        ))
        if num_tokens > NUM_TOKENS:
            raise InvalidScoresheetException(
                "Too many tokens: {} > {}".format(num_tokens, NUM_TOKENS),
            )

    def calculate_scores(self):
        scores_by_zone = {
            zone: info.get('tokens_ground', 0) * POINTS_GROUND +
                info.get('tokens_platform', 0) * POINTS_PLATFORM
            for zone, info in self._arena_data.items()
        }

        scores_by_tla = {
            tla: info.get('tokens_held', 0) * POINTS_HELD
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
