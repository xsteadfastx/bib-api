import logging
import os
import sys


logger = logging.getLogger('app')


def load_facilities():
    """Facility loader.

    Its loading facilities from the facilitie directory. These are some kind
    of plugins in a way. Its used to for easily adding new libraries to the
    API.

    :return: Dictionary with functions to interact with libraries.
    :rtype: dict
    """
    facilities = {}

    facilities_path = os.path.dirname(
        os.path.realpath(__file__)) + '/facilities'
    sys.path.insert(0, facilities_path)

    for facility in os.listdir(facilities_path):

        fname, ext = os.path.splitext(facility)

        if ext == '.py':

            facilities[fname] = {}

            mod = __import__(fname)

            # load facility metadata dict
            facilities[fname]['metadata'] = mod.metadata

            # load needed functions into the dict
            facilities[fname]['search'] = mod.search

            logger.info('loaded facility: {}'.format(fname))

    sys.path.pop(0)

    return facilities
