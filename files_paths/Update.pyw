import os, datetime
from time import sleep

def update(**kwargs):
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
                  "F:/TV Series":             "main hard_f_tv_series_tree.txt",
                  "E:/Movies(2)":             "main_hard_movies_e_tree.txt",
                  "G:/Anime_1Tera":           "1_tera_animes_tree.txt",
                  "G:/Movies_1Tera":          "1_tera_movies_tree.txt",
                  "G:/TV Series_1Tera":       "1_tera_tv_tree.txt",
                  "E:/TV Series":             "main hard_e_tv_series_tree.txt", }
    for dir_path, txt in paths_txts.items():
        if not os.path.exists(dir_path):
            continue
        paths = []
        sizes = []
        txt_path = f"{txt}"#change this according to 
        #current directory
        for root, dirs, files in os.walk(dir_path):
            paths.append(root)
            sizes.append(os.path.getsize(paths[-1]))
            for f in files:
                paths.append(f"{root}{os.sep}{f}")
                sizes.append(os.path.getsize(paths[-1]))
        calc_size(paths, sizes)
        with open(txt_path, "w",encoding="utf-8") as file_object:#needs to be unicode
            #the default is ascii
            for path, size in zip(paths, sizes):
                file_object.write(f"{path}|{size}\n")
            print(f"Updated {dir_path}")
    # if removed the .txt is going to be overwrriten even if path doesn't exist
            
###Main###
update()
updated_g=False
updated_h=False
while True:
    print("====big loop====")
    while True:
        print("-smal loop-")
        if os.path.exists("H:/") and os.path.exists("G:/"):
            path="Both"
            print("both")
            updated_h=True
            updated_g=True
            break
        elif os.path.exists("H:/") and updated_h==False:
            print("2 tera")
            path="H:/ (2 Tera)"
            updated_h=True
            break
        elif os.path.exists("G:/") and updated_g==False:
            print("1 tera")
            path="G:/ (1 tera)"
            updated_g=True
            break
        else:
            sleep(1)
    print("left checking loop")
    update()#remember that it updates everything
    with open("update.txt","a") as file_object:
        file_object.write(f"{datetime.datetime.now()}  updated: {path}\n")
    if updated_h==True and updated_g==True:
        exit()
    
    
   
        
