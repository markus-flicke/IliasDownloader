import shutil
import time
import os
import pandas as pd


class Writer:
    def __init__(self):
        self.stats_df = pd.read_msgpack('stats')#pd.DataFrame(columns = ['File', 'DateTime', 'Dir'])

    def save_stats(self):
        self.stats_df.to_msgpack('stats')

    def copy(self, filename, target_dir='output/', source_dir='downloads/'):
        filename = self.to_os_name(filename)

        def finished_loading(filename):
            files_in_downloads = os.listdir(source_dir)
            filenames = list(map(lambda x: '.'.join(x.split('.')[:-1]), files_in_downloads))
            if filename in filenames:
                idx = filenames.index(filename)
                if files_in_downloads[idx].endswith('crdownload'):
                    return False
            return filename in filenames

        c = 0
        while not finished_loading(filename):
            time.sleep(0.001)
            c += 1
            if c % 1000 == 0:
                dir_no_endings = list(map(lambda x: '.'.join(x.split('.')[:-1]), os.listdir(source_dir)))
                print('file not yet found: {} in {}'.format(filename, dir_no_endings))

        self.recursive_create(target_dir)
        files = os.listdir(source_dir)
        for file in files:
            try:
                shutil.move(source_dir + file, target_dir + file)
            except:
                print('Copy fail\nfrom: {}\nto: {}'.format(source_dir + file, target_dir + file))
                raise
        while os.listdir('downloads/'):
            time.sleep(0.001)

        self.stats_df = self.stats_df.append(dict(File = filename,
                              DateTime = pd.datetime.now(),
                              Dir = target_dir),
                         ignore_index = True)

    @classmethod
    def recursive_create(self, path):
        if os.path.exists(path):
            return
        mother_folder = ('/').join(path.split('/')[:-1])
        if os.path.exists(mother_folder):
            os.mkdir(path)
        if not os.path.exists(mother_folder):
            self.recursive_create(mother_folder)

    @staticmethod
    def to_os_name(ilias_name):
        res = ilias_name.replace('/', '_') \
            .replace('ü', 'ue') \
            .replace('ä', 'ae') \
            .replace('ö', 'oe')
        return res
