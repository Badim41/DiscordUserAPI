class ClientDevice:
    web = {
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "ru-RU",
        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "browser_version": "124.0.0.0",
        "os_version": "10",
        "referrer": "https://discord.com/",
        "referring_domain": "discord.com",
        "referrer_current": "",
        "referring_domain_current": "",
        "search_engine_current": "google",
        "mp_keyword_current": "discord",
        "release_channel": "stable",
        "client_build_number": 290453,
        "client_event_source": None,
        "design_id": 0
    }
    windows = {
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "ru",
        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "browser_version": "124.0.0.0",
        "os_version": "10",
        "referrer": "https://discord.com/",
        "referring_domain": "discord.com",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": 307828,
        "client_event_source": None
    }
    macos = {
        "os": "Mac OS X",
        "browser": "Discord Client",
        "release_channel": "ptb",
        "client_version": "0.0.113",
        "os_version": "23.4.0",
        "os_arch": "arm64",
        "app_arch": "arm64",
        "system_locale": "ru-RU",
        "browser_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.113 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36",
        "browser_version": "28.2.10",
        "client_build_number": 290668,
        "native_build_number": None,
        "client_event_source": None,
        "design_id": 0
    }
    linux = {
        "os": "Linux",
        "browser": "Discord Client",
        "release_channel": "canary",
        "client_version": "0.0.381",
        "os_version": "5.15.153.1-microsoft-standard-WSL2",
        "os_arch": "x64",
        "app_arch": "x64",
        "system_locale": "ru-RU",
        "browser_user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.381 Chrome/120.0.6099.291 Electron/28.2.10 Safari/537.36",
        "browser_version": "28.2.10",
        "window_manager": "Hyprland,unknown",
        "distro": "Ubuntu 22.04.4 LTS",
        "client_build_number": 290668,
        "native_build_number": None,
        "client_event_source": None,
        "design_id": 0
    }
    android = {
        "os": "Android",
        "browser": "Discord Android",
        "device": "Pixel 6",
        "system_locale": "ru-RU",
        "client_version": "227.6 - rn",
        "release_channel": "canaryRelease",
        "device_vendor_id": "a1234567-b89c-1234-d567-890123456789",
        "browser_user_agent": "",
        "browser_version": "",
        "os_version": "34",  # Android 14
        "client_build_number": 227206,
        "client_event_source": None,
        "design_id": 2
    }
    ios = {
        "os": "iOS",
        "browser": "Discord iOS",
        "device": "iPhone14,5",  # iPhone 13
        "system_locale": "ru-RU",
        "client_version": "227.0",
        "release_channel": "stable",
        "device_vendor_id": "AFF0710F-CEC0-4671-B2CF-0A03D72B5FD0",
        "browser_user_agent": "",
        # While it is not provided here, the User-Agent header is Discord/58755 CFNetwork/1494.0.7 Darwin/23.4.0
        "browser_version": "",
        "os_version": "17.4.1",
        "client_build_number": 58755,
        "client_event_source": None,
        "design_id": 2
    }
