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
            ]
        )
        self.add_option("dns-protocol")
        self.add_option('not-found-re', 'http-not-found-re')
        self.add_option('retest-phrase', 'http-retest-phrase')
        self.add_option('proxies', 'http-proxies')
