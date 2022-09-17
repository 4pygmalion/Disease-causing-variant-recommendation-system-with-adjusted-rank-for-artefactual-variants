import os
import yaml
import logging
import datetime

DIS_SIM_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(DIS_SIM_DIR, "logs")


def load_yaml(file_path: str) -> dict:
    """YAML file을 dictionary로 불러오는 메서드

    Args:
        file_path (str): yaml file path의 경로
        
    Return:
        (dict): yaml파일의 내용을 딕셔너리로 반환한 값.
    """
    if not file_path.endswith(".yaml"):
        raise ValueError(f"Unexpected file extension: {file_path}")
    with open(file_path, "r") as fh:
        return yaml.load(fh, Loader=yaml.FullLoader)


def get_logger(module_name: str, log_path: str = None) -> logging.Logger:

    if log_path and not log_path.endswith(".log"):
        msg = (
            f"passed log_path ({log_path}), "
            "expected log_path must be ended with '.log'"
        )
        raise ValueError(msg)

    elif not log_path:
        start_time = datetime.datetime.now().strftime("%Y-%m-%d")
        log_module_dir = os.path.join(LOG_DIR, module_name)

        if not os.path.exists(log_module_dir):
            os.makedirs(log_module_dir)

        log_path = os.path.join(
            log_module_dir, f"{module_name}-{start_time}.log"
        )

    logger_formatter = logging.Formatter(
        fmt="{asctime}\t{name}\t{filename}:{lineno}\t{levelname}\t{message}",
        datefmt="%Y-%m-%dT%H:%M:%S",
        style="{",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logger_formatter)
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename=log_path)
    file_handler.setFormatter(logger_formatter)
    file_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
