from sys import stderr
from loguru import logger


def logs():
    try:
        logger.remove()
        logger.add(stderr, format='<white>{time:HH:mm:ss}</white>'
                                      ' | <level>{level: <2}</level>'
                                      ' | <level>{message}</level>')
        logger.add('./Loging/LOgs.log')
        return logger
    except BaseException:
        return logger



if __name__ == '__main__':
    pass
