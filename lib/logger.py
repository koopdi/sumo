import logging

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG) # console log level

file_handler = logging.FileHandler("log.txt", mode="a")
file_handler.setLevel(logging.INFO) # file log level

# Create a formatter
# asctime doesn't work
# formatter = logging.Formatter("%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s")
formatter = logging.Formatter("%(name)s.%(levelname)s: %(message)s")

# Add formatter to the handlers
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

def flush():
    file_handler.stream.flush()

def init(name = None):
    # Create logger
    logger = logging.getLogger(name)
    # Set logger to accept the stream_handler levels.
    logger.setLevel(logging.DEBUG)

    # Add handlers to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    
    return logger

def test(logger):
    # Log some messages
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")
    logger.info("message %s %d", "arg", 5)
    logger.info("message %(foo)s %(bar)s", {"foo": 1, "bar": 20})
    logger.debug("not a critical error, not even really important --- ignore")
