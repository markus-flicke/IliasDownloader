import os
import time

class Reader():
    def __init__(self, driver):
        self.driver = driver

    def dir(self):
        events_webelements = self.driver.find_elements_by_class_name('il_ContainerItemTitle')[::3]
        event_names = list(map(lambda val: val.text, events_webelements))
        self.events = dict(zip(event_names, events_webelements))
        forbidden_dirs = ['übung', 'diskussion', 'umfrage', 'votes', 'abgabe', 'gruppe']
        for name in event_names:
            if any(map(lambda x: x in name.lower(), forbidden_dirs)) and not name.lower() == 'übungsaufgaben':
                del self.events[name]
        return self.events

    def recursive_read(self, target_dir ='output/'):
        print('reading: {}'.format(target_dir))
        if os.path.exists(target_dir):
            already_have = next(os.walk(target_dir))[2]
            already_have = list(map(lambda x: '.'.join(x.split('.')[:-1]), already_have))
        else:
            already_have = []
        content = self.dir()
        headers = list(content.keys())
        url = self.driver.current_url
        for header in headers:
            if self.to_os_name(header) not in already_have:
                self.dir()[header].click()
                if not url == self.driver.current_url:
                    self.recursive_read(target_dir=target_dir + header + '/')
                    url = self.driver.current_url
                else:
                    print('dont have "{}" need to download.'.format(header))
                    self.copy(header, target_dir)
        print('complete: {}'.format(target_dir))
        self.driver.back()

    @classmethod
    def copy(self, filename, target_dir='output/', source_dir='downloads/'):
        filename = self.to_os_name(filename)
        def finished_loading():
            for file in os.listdir(source_dir):
                if file.endswith('crdownload'):
                    return False
                dir_no_endings = list(map(lambda x: '.'.join(x.split('.')[:-1]), os.listdir(source_dir)))
                if not filename in dir_no_endings:
                    return False
            return True
        c = 0
        while not finished_loading():
            time.sleep(0.001)
            c += 1
            if c % 1000 == 0:
                dir_no_endings = list(map(lambda x: '.'.join(x.split('.')[:-1]), os.listdir(source_dir)))
                print('file not yet found: {} in {}'.format(filename, dir_no_endings))

        def recursive_create(path):
            if os.path.exists(path):
                return
            mother_folder = ('/').join(path.split('/')[:-1])
            if os.path.exists(mother_folder):
                os.mkdir(path)
            if not os.path.exists(mother_folder):
                recursive_create(mother_folder)

        recursive_create(target_dir)
        files = os.listdir(source_dir)
        for file in files:
            try:
                print('from: {}\nto: {}'.format(source_dir + file, target_dir + file))
                os.rename(source_dir + file, target_dir + file)
            except:
                print('files: {}'.format(files))
                print('file: {}'.format(file))
        while os.listdir('downloads/'):
            time.sleep(0.001)


    @staticmethod
    def to_os_name(ilias_name):
        res = ilias_name.replace('/','_')\
            .replace('ü', 'ue')\
            .replace('ä', 'ae')\
            .replace('ö', 'oe')
        return res

