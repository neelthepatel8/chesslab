import logging

VERBOSE = 15
logging.addLevelName(VERBOSE, "VERBOSE")

def verbose(self, message, *args, **kws):
    pass
logging.Logger.verbose = verbose

def get_logger(log_level):
    if log_level is None:
        return None
    
    log_level_mapping = {
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'VERBOSE': VERBOSE
    }
    log_level = log_level_mapping.get(log_level, logging.INFO) 

    logger = logging.getLogger('chess')
    logger.setLevel(log_level)

    # ch = logging.StreamHandler()
    # ch.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # ch.setFormatter(formatter)
    
    fh = logging.FileHandler('chess.log')
    fh.setLevel(log_level)  
    fh.setFormatter(formatter)

    # logger.addHandler(ch)
    logger.addHandler(fh)

    return logger