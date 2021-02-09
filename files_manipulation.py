import colorama, pdb, collections
import os,re,pprint
from time import sleep
import pdb,prettytable
class File():
    """Carries info of a file and has file management methods"""
    def __init__(self, path, file_type, dir_tag="", size=0, surface=False):
        self.name = os.path.basename(path)
        self.path = path
        self.dir_tag = dir_tag
        self.file_type = file_type
        self.size = size
        self.surface = surface
    
    def get_size(self):
        """returns size(int or float) of file and unit(str) of that size"""
        #size is in bytes
        #10^3 > KB
        #10^6 > MB
        if self.size<10**6:# converts bytes to KBs 
            size=self.size/1024
            unit="KB"
            size=int(size)
        elif self.size<10**9:#converts bytes to MBs
            #1048576 is 1024 * 1024
            size=self.size/1048576
            size=round(size,1)  #rounds to a total of 4 digits
            unit="MB"
        else:#if size>10^9 converts to GBs
            #1073741824 is 1024 * 1024 * 1024
            size=self.size/1073741824
            size=round(size,2)  #rounds to a total of 4 digits
            unit="GB"
        return size,unit

def find_cmds(input_line):
    """Returns a dictionary containing the details of the command written"""
    match = re.search("-.*",input_line)
    cmd={}
    if match:
        cmd_tag=match.group()
        net_input_line=input_line.replace(cmd_tag,"")
    else:
        cmd=None
        return input_line, cmd
    if cmd_tag == "-dups":  #to change what function catches as commands
        #just change the if coniditon nothing else
        cmd["func name"]="print_duplicates"
    elif cmd_tag == "-all movies":
        cmd["func name"]="get_clips"
        cmd["file type"]="movie"
    elif cmd_tag == "-all tv":
        cmd["func name"]="get_clips"
        cmd["file type"]="tv series"
    elif cmd_tag == "-all animes":
        cmd["func name"]="get_clips"
        cmd["file type"]="anime"
    elif cmd_tag=="-this pc e":
        cmd["func name"]="get_clips"
        cmd["dir tag"]="this pc e"
    elif cmd_tag=="-this pc f":
        cmd["func name"]="get_clips"
        cmd["dir tag"]="this pc f"
    elif cmd_tag == "-this pc tv":
        cmd["func name"]="get_clips"
        cmd["file type"]="tv series"
        cmd["dir tag"]="this pc"
    elif cmd_tag == "-this pc movies":
        cmd["func name"]="get_clips"
        cmd["file type"]="movies"
        cmd["dir tag"]="this pc"
    elif cmd_tag == "-2 tera movies":
        cmd["func name"]="get_clips"
        cmd["file type"]="movie"
        cmd["dir tag"]="2 tera movies"
    elif cmd_tag == "-2 tera tv":
        cmd["func name"]="get_clips"
        cmd["file type"]="tv series"
        cmd["dir tag"]="2 tera tv"
    elif cmd_tag == "-2 tera animes":
        cmd["func name"]="get_clips"
        cmd["file type"]="anime"
        cmd["dir tag"]="2 tera animes"
    elif cmd_tag == "-1 tera movies":
        cmd["func name"]="get_clips"
        cmd["file type"]="movie"
        cmd["dir tag"]="1 tera movies"
    elif cmd_tag == "-1 tera tv":
        cmd["func name"]="get_clips"
        cmd["file type"]="tv series"
        cmd["dir tag"]="1 tera tv"
    elif cmd_tag == "-1 tera animes":
        cmd["func name"]="get_clips"
        cmd["file type"]="anime"
        cmd["dir tag"]="1 tera animes"
    return net_input_line, cmd

def find_dir_tags(input_line):
    """returns directory tag(if exists) and input line without the tag in it"""
    match = re.search(r'''^         ((this \s pc (\s(e|f))? (?=\s))  
                        # this pc followed by e or f opt.,followed by space(not consumed)
                                                        |
                                ((1|2) \s tera (\s (movies|tv|animes) )? (?=\s)))''',
                           # 1|2 tera followed by movies tv or animes(opt.) followed by space(not consumed)
                           input_line,
                           re.VERBOSE | re.I)
    if match:
        dir_tag = match.group()
        to_replace = dir_tag+" "  # because dir_tag doesn't have the space in it
        net_input_line = input_line.replace(to_replace, "")
    else:
        dir_tag = None
        net_input_line = input_line
    return net_input_line, dir_tag

def search(trees, search_for, spec_dir=""):
    """returns a list of File class objects thatcarry the results's data/details."""
    os.system("cls")
    search_for = search_for.lower()
    search_for = search_for.split()
    search_words_count = len(search_for)
    results = []
    for file_obj in trees:
        matches_count = 0
        if file_obj.surface==True and search_for[0] in file_obj.name.lower():
            for word in search_for:
                if word in file_obj.name.lower():
                    matches_count += 1
            if matches_count == search_words_count:
                if spec_dir:#i think if you remove this
                    if spec_dir in file_obj.dir_tag.lower():
                        results.append(file_obj)
                else:#and this the code will work thus fine because "" is in any string anyway
                    results.append(file_obj)
    return results

def print_results(results, dups=False):
    """
    takes in results of a search (File objects or Dup objects) and prints their info in a formatted
    manner
     """
    colorama.init()
    os.system("cls")
    print(colorama.Fore.YELLOW+"\n\n\t\t\t\t\t\t\tResults\n\n\n")
    if not dups :
        table=prettytable.PrettyTable([colorama.Fore.YELLOW+"Names",colorama.Fore.YELLOW+"Dir Tag",colorama.Fore.YELLOW+"Size"])
        for result in results:
            size,unit=result.get_size()
            table.add_row([colorama.Fore.LIGHTBLUE_EX+f"{result.name:75}",
                           colorama.Fore.LIGHTBLUE_EX+f"{result.dir_tag:10}",
                           colorama.Fore.LIGHTBLUE_EX+f"{size} {unit}"])
            # print(colorama.Fore.LIGHTBLUE_EX + f"{result.name:75}             {result.dir_tag:50}\n")
        print(table)
    else:
        for result in results:
            if len(result.dir_tags) > 4:#prints only 3 and .... the rest
                dir_tags = results.dir_tags[:3]
                dir_tags.append("....")
            else:
                dir_tags = result.dir_tags
            dir_tags = " | ".join(dir_tags)
            print(colorama.Fore.RED + f"{result.name:70} {dir_tags:50}\n")

def get_duplicates(clips):
    """
    returns a list of Dup namedtuples that contain the info of the duplicate surface files that exist in trees
    """
    clips_names=[clip.name for clip in clips if clip.surface==True]
    files_count = collections.Counter(clips_names)
    duplicates = []
    dups_names=[]
    for file_name,count in files_count.items():
        if count>1:
            dups_names.append(file_name)
    for dup_name in dups_names :
        results = search(clips, dup_name)#all results are of same name
        #but they have diff dir_tags/locations
        locations = [result.path for result in results]
        dir_tags = [result.dir_tag for result in results]
        file_type = results[0].file_type
        Dup=collections.namedtuple("dup","name file_type locations dir_tags")
        dup_obj = Dup(dup_name, file_type,locations,dir_tags)
        duplicates.append(dup_obj)
    return duplicates
    
def to_unit(size):
    #size is in bytes
    #10^3 > KB
    #10^6 > MB
    if size<10**6:# converts bytes to KBs 
        size=size/1024
        unit="KB"
    elif size<10**9:#converts bytes to MBs
        #1048576 is 1024 * 1024
        size=size/1048576
        unit="MB"
    else:#if size>10^9 converts to GBs
        #1073741824 is 1024 * 1024 * 1024
        size=size/1073741824
        unit="GB"
    size=round(size,4)  #rounds to a totale of 4 digits
    size=str(size)
    return size,unit

def print_tree(tree):
    """prints tree with indentation that indicate which folder/file is inside which"""
    os.system("cls")
    cont_path=tree[0]
    print(colorama.Fore.YELLOW+"\n\n\t\t\t\t\t\t\tResults\n\n\n")
    cont_size,cont_unit=cont_path.get_size()
    print(colorama.Fore.YELLOW +
          f"\n\n{cont_path.name:70}",end="")  # has no indentation
    print(colorama.Fore.RED+
     f"{cont_size:12} {cont_unit}\n")
    print(colorama.Fore.YELLOW+"-"*90+"\n")
    for branch in tree[1:]:
        #you can simply know the level by the number of backslashes in the name
        #we remove the backslashes in start to restore the level to 0 for the levels
        #to be in respect to the start_path itself not C:\ or F:\
        level = branch.path.replace(cont_path.path, "").count(os.sep) - 1
        indent = " " * 8 * level
        size,unit=branch.get_size()
        print(colorama.Fore.WHITE+
         f"{indent}{branch.name:70}   {colorama.Fore.BLUE}{size:>6} {unit:>}\n")
    input()

def get_clips(trees, cmd):
    """
    returns a chunk of clips according to dir tag and file type carried by the Cmd Object only(ex:-this pc movies)
    """
    clips=[]
    if len(cmd.keys())==2:
        if "dir tag" in cmd.keys() :
            for file_obj in trees:
                if file_obj.surface==True and cmd["dir tag"] == file_obj.dir_tag.lower():
                    clips.append(file_obj)
        elif "file type"  in cmd.keys():
            for file_obj in trees:
                if file_obj.surface==True and cmd["file type"]==file_obj.file_type:
                    clips.append(file_obj)    
    elif "dir tag" in cmd.keys():#it means a a specific dir is to be searched
        for file_obj in trees:
            if file_obj.surface==True and cmd["dir tag"] in file_obj.dir_tag.lower() and file_obj.file_type==cmd["file type"]:
                clips.append(file_obj)
     
    return clips

def get_tree(result,trees):
    """
    returns a list of the tree of the current object's file path
                    (actual full path is used to search)          
    """
    tree = []
    tree.append(result)#because result.path isn't in in it's dirname, look down
    for file_obj in trees:
        if result.path in os.path.dirname(file_obj.path):
            tree.append(file_obj)
    return tree