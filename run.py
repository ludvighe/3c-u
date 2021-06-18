from modules.cli import Cli
import modules.util.settings as settings

SETTINGS_PATH = 'res/settings.json'

if __name__ == '__main__':
    # Initialize settings for global use in modules
    settings.init(path=SETTINGS_PATH)

    # Initialize cli
    Cli()
