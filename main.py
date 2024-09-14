from config import get_config

def main():
    config = get_config()
    print(config.ENVIRONMENT)
    print(config.NOTION_INTERNAL_INTEGRATION_SECRET)
    print(config.YOUTUBE_CHANNELS_CONFIG_JSON)

if __name__ == "__main__":
    main()