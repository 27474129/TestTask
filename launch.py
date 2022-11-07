if __name__ == "__main__":
    from sources import main
    from logger_configuration import configure_logger
    configure_logger('DEBUG')
    main.launch()
