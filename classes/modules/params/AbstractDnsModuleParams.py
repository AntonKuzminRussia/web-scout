from classes.modules.params.AbstractModuleParams import AbstractModuleParams


class AbstractDnsModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'template',
                'msymbol',
                'delay',
                'ignore-words-re',
                'ignore-ip',
                'http-protocol',
                'headers-file',
                'zone',
                "dns-protocol",
                'http-not-found-re',
                'http-retest-phrase',
                'http-proxies',
            ]
        )
