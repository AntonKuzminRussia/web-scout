from classes.modules.params.AbstractModuleParams import AbstractModuleParams


class AbstractHostsBruterModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'proxies',
                'delay',
                'template',
                'headers-file',
                "ignore-words-re",
                "retest-codes",
                "retest-phrase"
                'false-phrase',
                'false-size',
                'ip',
                'msymbol',
            ]
        )
        self.add_option('http-protocol', 'protocol')