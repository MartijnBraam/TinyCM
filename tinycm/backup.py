import os
import shutil
import logging
import datetime

current_id = None


def backup_file(path):
    logger = logging.getLogger('tinycm')
    backup_index()
    if not current_id:
        raise Exception('Backup requested before unique id is generated')
    path = os.path.realpath(path)
    logger.debug('Starting backup for {}'.format(path))
    backup_dir = '/var/backups/tinycm'
    backupfile = os.path.join(backup_dir, current_id, path[1:])
    backupfile_path = os.path.dirname(backupfile)
    os.makedirs(backupfile_path, 0o700, exist_ok=True)
    logger.debug('Backup to: {}'.format(backupfile))
    shutil.copy2(path, backupfile)


def backup_index():
    if not current_id:
        raise Exception('Backup requested before unique id is generated')
    backup_dir = '/var/backups/tinycm'
    backuproot = os.path.join(backup_dir, current_id)
    os.makedirs(backuproot, 0o700, exist_ok=True)
    backupindex = os.path.join(backuproot, 'index.txt')
    with open(backupindex, 'w') as index_file:
        contents = [
            'id={}'.format(current_id),
            'time={}'.format(datetime.datetime.now().isoformat()),
        ]
        index_file.writelines(contents)
