from Navigator import Navigator
from Reader import Reader
import os


if __name__ == '__main__':
    if not 'output' in os.listdir(''):
        os.mkdir('output/')
    if not 'downloads' in os.listdir(''):
        os.mkdir('downloads/')
    if not 'credentials.txt' in os.listdir(''):
        with open('credentials.txt', 'w+') as file:
            file.write('username\npassword')
        raise Exception('You need to update username and password in credentials.txt')
    navi = Navigator()
    reader = Reader(navi.driver)
    navi.sign_in()
    reader.recursive_read()