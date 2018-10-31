from Navigator import Navigator
from Reader import Reader
import os
import argparse


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-headless', help = 'Use for testing', action = 'store_true')
    return parser.parse_args()

def process_kwargs():
    args = argparser()
    return args.headless


if __name__ == '__main__':
    def initialise_directories():
        if not 'output' in os.listdir('./'):
            os.mkdir('output/')
        if not 'downloads' in os.listdir('./'):
            os.mkdir('downloads/')
        if not 'credentials.txt' in os.listdir('./'):
            with open('credentials.txt', 'w+') as file:
                file.write('username\npassword')
            raise Exception('You need to update username and password in credentials.txt')

    initialise_directories()
    navi = Navigator(headless = process_kwargs())
    reader = Reader(navi.driver)
    navi.sign_in()
    try:
        reader.recursive_read()
    except:
        raise
    finally:
        reader.writer.save_stats()

    print('--------SUCCESS---------')
    print('files copied:')
    for filename in reader.copied_files:
        print(filename)

