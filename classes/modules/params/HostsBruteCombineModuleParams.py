from classes.modules.params.AbstractHostsBruterModuleParams import AbstractHostsBruterModuleParams


class HostsBruteCombineModuleParams(AbstractHostsBruterModuleParams):
    def __init__(self):
        AbstractHostsBruterModuleParams.__init__(self)
        self.add_options(
            [
                'mask',
                'dict',
                'combine-template',
            ]
        )