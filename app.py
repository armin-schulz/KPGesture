import logging

from painting import painting
from exploration import exploration
from config import MODE

logger = logging.getLogger(__name__)


def main():
    match MODE:
        case 'painting':
            painting()

        case  'exploration':
            exploration()
        case _:
            logger.error('No mode selected')


if __name__ == '__main__':
    main()
