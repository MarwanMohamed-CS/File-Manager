import colorama,pdb,time
import os,collections,re
import files_manipulation as fm
import pprint
from time import sleep

#simplizing

def update():
    """
    writes to a collections of .txts the trees of files and folders inside
    specific dirs
    """
    def calc_size(paths, sizes):
       """calculates the real size of each path directly changing sizes list"""
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
    
    paths_txts = {"H:/Anime_2Tera":           "2_tera_animes_tree.txt",
                  "H:/Movies_2Tera":          "2_tera_movies_tree.txt",
                  "H:/TV Series_2Tera":       "2_tera_tv_tree.txt",
                  "F:/Movies":                "main_hard_movies_f_tree.txt",
                  "F:/TV Series":             "Main hard_f_tv_series_tree.txt",
                  "E:/Movies(2)":             "main_hard_movies_e_tree.txt",
                  "G:/Anime_1Tera":           "1_tera_animes_tree.txt",
                  "G:/Movies_1Tera":          "1_tera_movies_tree.txt",
                  "G:/TV Series_1Tera":    "1_tera_tv_tree.txt",
                  "E:/TV Series":        "Main hard_e_tv_series_tree.txt", }
    curr_dir = os.getcwd()
    for dir_path, txt in paths_txts.items():
        if not os.path.exists(dir_path):
            continue
        paths = []
        sizes = []
        txt_path = f"{curr_dir}{os.sep}files_paths{os.sep}{txt}"
        for root, dirs, files in os.walk(dir_path):
            paths.append(root)
            sizes.append(os.path.getsize(paths[-1]))
            for f in files:
                paths.append(f"{root}{os.sep}{f}")
                sizes.append(os.path.getsize(paths[-1]))
        calc_size(paths, sizes)
        try:
            with open(txt_path, "w") as file_object:
                for path, size in zip(paths, sizes):
                    file_object.write(f"{path}|{size}\n")
                print(f"Updated {dir_path}")
        except:
            pass
    # if removed the .txt is going to be overwrriten even if path doesn't exist

def read():
    """reads trees of each path and returns a list containing
    the file objects """
   
    txts = {  # formats:
        # 2 tera animes                                     #dir tag of next
        "files_paths\\2_tera_animes_tree.txt":  # "":
        {"dir tag": "2 Tera Animes",  # {"dir tag"  :"",
         "clips path": "H:/Anime_2Tera",  # "clips path":"",
         "file type": "anime", }  # "file type" :"",}
        ,  # 2 tera movies                                    #,#dir tag of next
        "files_paths\\2_tera_movies_tree.txt":
        {"dir tag": "2 Tera Movies",
         "clips path": "H:/Movies_2Tera",
         "file type": "movie", },  # 2 tera tv
        "files_paths\\2_tera_tv_tree.txt":
        {"dir tag": "2 Tera TV",
         "clips path": "H:/TV Series_2Tera",
         "file type": "tv series", },  # main hard movies f
        "files_paths\\main_hard_movies_f_tree.txt":
        {"dir tag":    "This PC F",
         "clips path": "F:/Movies",
         "file type":    "movie", },  # main hard tv series f
        "files_paths\\Main hard_f_tv_series_tree.txt":
        {"dir tag": "This PC F",
         "clips path": "F:/TV Series",
         "file type": "tv series", },  # main hard movies e
        "files_paths\\main_hard_movies_e_tree.txt":
        {"dir tag": "This PC E",
         "clips path": "E:/Movies(2)",
         "file type": "movie", },  # main hard tv series e
        "files_paths\\Main hard_e_tv_series_tree.txt":
        {"dir tag": "This PC E",
         "clips path": "E:/TV Series",
         "file type": "tv series", },  # 1 tera animes
        "files_paths\\1_tera_animes_tree.txt":
        {"dir tag": "1 Tera Animes",
         "clips path": "G:/Anime_1Tera",
         "file type": "anime", },  # 1 tera movies
        "files_paths\\1_tera_movies_tree.txt":
        {"dir tag": "1 Tera Movies",
         "clips path": "G:/Movies_1Tera",
         "file type": "movie", },  # 1 tera tv
        "files_paths\\1_tera_tv_tree.txt":
        {"dir tag": "1 Tera TV",
         "clips path": "G:/TV Series_1Tera",
         "file type": "tv series", },}
    trees = []
    curr_dir = os.getcwd()
    for path, details in txts.items():
        path = f"{curr_dir}/{path}"
        if not os.path.exists(path):
            continue
        with open(path) as file_object:
            lines = file_object.read()
            lines = lines.split("\n")
            del lines[-1]
            for line in lines:
                file_path, file_size = line.split("|")
                if os.path.dirname(file_path) == details["clips path"]:
                    surface = True
                else:
                    surface = False
                trees.append(fm.File(file_path,
                                  details["file type"],
                                  details["dir tag"],
                                  int(file_size),
                                  surface,
                                  ))
    return trees

def open_file(result):
    """takes in a File object instance and opens it's directory and the file itself"""
    if os.path.exists(result.path):
        if os.path.isdir(result.path):#results is a folder
            error=True      #to check if clip was found
            dir_list = os.listdir(result.path)
            for file_name in dir_list:
                match=re.search( r'^(?!.*trailer).+(mkv|avi|mp4)$',
                                 file_name,
                                 re.DOTALL | re.I)
                if match:#file found
                    clip_path = f"{result.path}/{match.group()}"#actual clip path
                    os.startfile(clip_path)
                    os.startfile(result.path)
                    error=False
        else:#if result is a file
            os.startfile(result.path)
    else:
        print("\n\t\t\t\t***The directory you are trying to access is unavailable")
        sleep(4.5)
    if not error:
        input(colorama.Fore.LIGHTBLUE_EX+"The file was opened successfuly. Yay man you are awesome.")
    else:#if clip wasn't found in folder
        print('''\n\t\t\t\t***An unexpected error occured. It may be because the file
         is compressed.***''')
        sleep(4.5)

if __name__ == "__main__":
    os.system("cls")
    #update()
    trees = read()
    while(True):
        results=[]
        os.system("cls")
        print(colorama.Fore.GREEN+"Name: ", end="")
        input_line = input(colorama.Fore.WHITE+"")
        if not input_line :
            continue
        net_input_line, cmd = fm.find_cmds(input_line)
        net_input_line, dir_tag = fm.find_dir_tags(input_line)
        if not cmd and not dir_tag:#normal search
            results = fm.search(trees, net_input_line)
            fm.print_results(results)
        elif cmd: # we check cmd first but if dir_tag is checked first then it might 
                # catch things like -this pc or -1 tera no need to fix it
            if cmd["func name"] == 'print_duplicates':
                dups=fm.get_duplicates(trees)
                fm.print_results(dups, dups=True)
            elif cmd["func name"] == "get_clips":
                filtered_clips=fm.get_clips(trees,cmd)
                fm.print_results(filtered_clips)
        elif dir_tag:#search in specific dir
            results = fm.search(trees, net_input_line, dir_tag)
            fm.print_results(results)            
        end_cmd = input(colorama.Fore.WHITE)
        try:#to skip if results doesn't exist
            if len(results)==1: #if removed the prog will work but the function call will be
                                #executed, which will slow the program.
                if end_cmd == 'open' :
                    open_file(results[0])
                elif end_cmd=='tree' :
                    tree=fm.get_tree(results[0],trees)
                    fm.print_tree(tree)
        except NameError:#NameError for not finding the results list
            raise