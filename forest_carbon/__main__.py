from . import config
from .combined_agb_calculator import save_model


def main():
    save_model(config.SAVE_PATH)


if __name__ == "__main__":
    main()
