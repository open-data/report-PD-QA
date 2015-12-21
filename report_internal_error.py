import os

class InternalErrorReporter(object):

    @classmethod
    def setup(cls, internal_dir):
        try:
            cls.error_fs = open(internal_dir +'/error.txt', 'w')
        except IOError:
            raise

    @classmethod
    def report_error(cls,msg):
        cls.error_fs.write(msg+'\n')

    @classmethod
    def close_error_file(cls):
        cls.error_fs.close()








