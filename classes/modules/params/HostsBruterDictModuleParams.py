from classes.modules.params.AbstractHostsBruterModuleParams import AbstractHostsBruterModuleParams


class HostsBruterDictModuleParams(AbstractHostsBruterModuleParams):
    def __init__(self):
        AbstractHostsBruterModuleParams.__init__(self)
        self.add_option('dict')