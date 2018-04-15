import os
import tempfile
from filelock import FileLock
import attr

# For cases with reading whole file to memory
# for another cases iterator needed

@attr.s
class Locker(object):
    file = attr.ib()
    lock_file_name = attr.ib(default='')
    lock = attr.ib()
    lock_suffix = attr.ib(default='.pyfilerewritelock')

    def lock(self):
        self.lock = FileLock(self.lock_file_name, timeout=1)
        self.lock.acquire()

    def unlock(self):
        self.lock.release()
        os.remove(self.lock_file_name)

    def __attrs_post_init__(self):
        self.lock_file_name = self.file.name + self.lock_suffix


@attr.s
class Backuper(object):
    file = attr.ib()
    bak_file_name = attr.ib(default='')

    def backup(self):
        (fd, self.bak_file_name) = tempfile.mkstemp(dir='.')
        os.close(fd)
        with open(self.bak_file_name, 'w') as bak_file:
            # second read, have no idea how to prevent it without ugling API
            bak_file.write(self.file.read())

    def restore(self):
        os.rename(self.bak_file_name, self.file.name)

    def clean(self):
        os.remove(self.bak_file_name)

def rewrite(file, new_data):
    locker = Locker(file = file)
    backuper = Backuper(file = file)

    locker.lock()
    backuper.backup()
    try:
        file.seek(0)
        file.write(new_data)
        file.truncate()
        file.flush()
        os.fsync(file.fileno())
    except:
        backuper.restore()
        locker.unlock()
        # erorr messages neede to raise
        raise ValueError('Rewrite unsuccesful')
    finally:
        locker.unlock()
        backuper.clean()
