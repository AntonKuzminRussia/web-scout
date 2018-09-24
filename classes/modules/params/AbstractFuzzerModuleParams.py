from classes.modules.params.AbstractModuleParams import AbstractModuleParams


class AbstractFuzzerModuleParams(AbstractModuleParams):
    def __init__(self):
        AbstractModuleParams.__init__(self)
        self.add_options(
            [
                'delay',
                'method',
                'proxies',
                "headers-file",
                "urls-file",
                'url'
            ]
        )