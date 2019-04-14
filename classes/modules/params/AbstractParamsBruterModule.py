from classes.modules.params.AbstractModuleParams import AbstractModuleParams


class AbstractParamsBruterModule(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)

        self.add_options(
            [
                'url',
                "max-params-length",
                "value",
                "method",
                "not-found-re",
                "not-found-size",
                "not-found-codes",
                "ignore-words-re",
                "retest-codes",
                "retest-phrase",
                "delay",
                "ddos-detect-phrase",
                "ddos-human-action",
                "selenium",
                "browser-recreate-re",
                "proxies",
                "headers-file",
            ]
        )