"""
This is an example configuration for LaTeXBuddy and the tools that are supported
out-of-the-box. You may move this file and specify its path using the --config flag.
"""

modules = {
    "buddy": {
        "language": "en",
        "whitelist": "whitelist",
        "output": "errors.json",
        "enable-modules-by-default": True,
    },
    "LanguageTool": {
        # "enabled": True,
        "mode": "COMMANDLINE",
        # "remote_url": "https://api.languagetoolplus.com/v2/check",
        "disabled-rules": [
            "WHITESPACE_RULE",
            # "TYPOGRAFISCHE_ANFUEHRUNGSZEICHEN",
        ],
        "disabled-categories": [
            # "TYPOS",
        ],
    },
    "AspellModule": {
        # "enabled": True,
    },
    "ChktexModule": {
        # "enabled": True,
    },
    "TestModule": {
        "enabled": False,
    }
}
