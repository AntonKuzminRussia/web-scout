import os

from classes.kernel.WSException import WSException
from classes.kernel.WSModule import WSModule


class FuzzerModules(WSModule):
    def validate_main(self):
        """ Check users params """
        super(FuzzerModules, self).validate_main()

        if not len(self.options['urls-file'].value) and not len(self.options['url'].value):
            raise WSException("You must specify 'url' or 'urls-file' param")

        if len(self.options['urls-file'].value) and not os.path.exists(self.options['urls-file'].value):
            raise WSException(
                "File with urls '{0}' not exists!".format(self.options['urls-file'].value)
            )