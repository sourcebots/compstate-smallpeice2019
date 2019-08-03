import collections


class InvalidScoresheetException(Exception):
    pass


class Scorer(object):
    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

    def validate(self, extra):
        pass

    def calculate_scores(self):
        return {}


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
