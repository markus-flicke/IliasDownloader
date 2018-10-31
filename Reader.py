import os

from Writer import Writer

class Reader:
    def __init__(self, driver):
        self.driver = driver
        self.copied_files = []
        self.writer = Writer()

    def dir(self):
        events_webelements = self.driver.find_elements_by_class_name('il_ContainerItemTitle')[::3]
        event_names = list(map(lambda val: val.text, events_webelements))
        self.events = dict(zip(event_names, events_webelements))
        forbidden_dirs = ['diskussion', 'umfrage', 'votes', 'abgabe', 'themenvergabe', 'gruppe']
        for name in event_names:
            if any(map(lambda x: x in name.lower(), forbidden_dirs)) and not name.lower() == 'übungsaufgaben':
                del self.events[name]
        return self.events

    def recursive_read(self, target_dir='output/'):
        print('reading: {}'.format(target_dir))
        if os.path.exists(target_dir):
            already_have = next(os.walk(target_dir))[2]
            already_have = list(map(lambda x: '.'.join(x.split('.')[:-1]), already_have))
        else:
            already_have = []

        content = self.dir()
        headers = list(content.keys())

        def is_downloadable(element):
            return 'onclick' in element.get_attribute('innerHTML')

        for header in headers:
            if self.writer.to_os_name(header) not in already_have:
                element = self.dir()[header]
                if is_downloadable(element):
                    element.click()
                    self.writer.copy(header, target_dir)
                    self.copied_files.append(header)
                else:
                    element.click()
                    self.recursive_read(target_dir=target_dir + header + '/')
                    url = self.driver.current_url

        print('complete: {}'.format(target_dir))
        self.driver.back()