from classes.modules.params.AbstractModuleParams import AbstractModuleParams


class ContentDiscoveryModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'msymbol',
                'not-found-re',
                'not-found-ex',
                'not-found-size',
                'not-found-codes',
                'ignore-words-re',
                'retest-codes',
                'retest-phrase',
                'delay',
                'selenium',
                'ddos-detect-phrase',
                'ddos-human-action',
                'browser-recreate-re',
                'proxies',
                'headers-file',
                'template',
                'method',

                "urls-file",
                "discovery-exts",
            ]
        )
