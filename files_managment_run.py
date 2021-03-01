import colorama
import pdb
import time
import os
import collections
import re
from time import sleep
import files_manipulation as fm
import settings


def update():
    '''
    Writes to a collections of .txts the trees of files and folders inside
    specific dirs
    '''
    def calc_size(paths, sizes):
        '''Calculates the real size of each path directly changing sizes list'''
        net_sizes = sizes[:]
        for index, path_outer in enumerate(paths):
            for path_inner in paths[index:]:
                if path_outer in path_inner:
                    for hooked_index, path_inner_2 in enumerate(paths[index:]):
                        if path_outer == path_inner_2:
                            continue
                        if path_outer in path_inner_2:
                            sizes[index] += net_sizes[hooked_index+index]
                        else:
                            break
                    break

    txts = settings.txts
    CURR_DIR = os.getcwd()
    for txt, details in txts.items():
        if not os.path.exists(details['clips path']):
            continue
        paths = []
        sizes = []
        txt_path = f'{CURR_DIR}{os.sep}{txt}'
        for root, dirs, files in os.walk(details['clips path']):
            paths.append(root)
            sizes.append(os.path.getsize(paths[-1]))
            for f in files:
                paths.append(f'{root}{os.sep}{f}')
                try:
                    sizes.append(os.path.getsize(paths[-1]))
                except FileNotFoundError:
                    with open('errors.txt', 'a') as file_obj:
                        file_obj.write(f'{Exception}\n')
        calc_size(paths, sizes)
        try:
            with open(txt_path, 'w') as file_object:
                for path, size in zip(paths, sizes):
                    file_object.write(f'{path}|{size}\n')
                print(f'Updated {details["clips path"]}')
        except:
            pass
    # if removed the .txt is going to be overwrriten even if path doesn't exist


def read():
    '''reads trees of each path and returns a list containing
    the file objects '''
    txts = settings.txts
    paths = []
    CURR_DIR = os.getcwd()
    for path, details in txts.items():
        path = f'{CURR_DIR}/{path}'
        if not os.path.exists(path):
            continue
        with open(path) as file_object:
            lines = file_object.read()
            lines = lines.split('\n')
            del lines[-1]
            for line in lines:
                file_path, file_size = line.split('|')
                if os.path.dirname(file_path) == details['clips path']:
                    surface = True
                else:
                    surface = False
                paths.append(fm.File(file_path,
                                     details['file type'],
                                     details['dir tag'],
                                     int(file_size),
                                     surface,
                                     ))
    return paths


def open_file(results, end_cmd):
    '''takes in a File object instance and opens it's directory and the file itself'''
    error = True
    num_match = re.search(r'open \d{1,}', end_cmd)
    if num_match:
        num = num_match.group().split()[1]
        num = int(num)
    else:
        print("invalid command..")
        sleep(2)
        return

    for result in results:
        if result.index == num - 1:
            clip = result
    if os.path.exists(clip.path):
        if os.path.isdir(clip.path):  # clips is a folder
            for file_name in os.listdir(clip.path):
                match = re.search(r'^(?!.*trailer).+(mkv|avi|mp4)$',
                                  file_name,
                                  re.DOTALL | re.I)
                if match:
                    clip_path = f'{clip.path}/{match.group()}'
                    os.startfile(clip.path)
                    sleep(0.5)
                    os.startfile(clip_path)
                    input(colorama.Fore.LIGHTBLUE_EX +
                          'The file was opened successfuly. Yay man you are awesome.')
                    error = False
        else:  # if clip is a file
            os.startfile(clip.path)
    else:
        print('\n\t\t\t\t***The directory you are trying to access is unavailable')
        sleep(4.5)

    if error:  # if clip wasn't found in folder
        print('''\n\t\t\t\t***An unexpected error occured. It may be because the file
         is compressed.***''')
        sleep(4.5)


if __name__ == '__main__':
    os.system('cls')
    update()
    paths = read()
    while True:
        os.system('cls')
        inp = input(f'{colorama.Fore.GREEN}Name: {colorama.Fore.WHITE}')
        if not inp:
            continue
        net_inp, cmd = fm.parse_inp(inp)
        results = []
        if not cmd:  # normal search
            results = fm.search(paths, net_inp)
            fm.print_results(results)
        elif cmd['type'] == 'cmd':
            if cmd['func name'] == 'print_duplicates':
                dups = fm.get_duplicates(paths)
                fm.print_results(dups, dups=True)
            elif cmd['func name'] == 'get_clips':
                results = fm.get_clips(paths, cmd)
                fm.print_results(results)
        elif cmd['type'] == 'dir tag':
            results = fm.search(paths, net_inp, cmd['dir tag'])
            fm.print_results(results)

        end_cmd = input(colorama.Fore.WHITE)
        if 'open' in end_cmd:
            open_file(results, end_cmd)
        elif 'tree' in end_cmd:
            tree = fm.get_tree(paths, results, end_cmd)
            fm.print_tree(tree)
        elif 'export' in end_cmd:
            fm.create_pdf(results,
                          inp=end_cmd)
        elif end_cmd == 'clean':
            fm.clean()
