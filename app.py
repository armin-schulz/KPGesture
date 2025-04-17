import logging
import sys

from app_util import setup_logging
from painting import painting
from exploration import exploration
from config import MODE

logger = logging.getLogger(__name__)


def main(args):
    match MODE:
        case 'painting':
            painting(args)

        case  'exploration':
            exploration()
        case _:
            logger.error('No mode selected')


if __name__ == '__main__':
    setup_logging()
    main(sys.argv[1:])
