import logging


logger = logging.getLogger(__name__)



# ============================================
#Log security events
# ============================================





def log_event(level, event, file_path, file_hash=None):

    log_message = event + " | " + file_path

    if file_hash is not None:

        log_message = (
            log_message
            + " | SHA-256: "
            + file_hash
        )

    if level == "INFO":

        logger.info(log_message)

    elif level == "WARNING":

        logger.warning(log_message)

    elif level == "ERROR":

        logger.error(log_message)

    elif level == "CRITICAL":

        logger.critical(log_message)