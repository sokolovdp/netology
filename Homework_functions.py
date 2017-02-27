
# coding: utf-8

# In[19]:

def get_all_documents() :
    documents = [
            {"type": "passport", "number": "2207-876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
          ]
    return documents

def get_all_directories() :
    directories = {
            '1': ['2207-876234', '11-2'],
            '2': ['10006'],
            '3': []
          }
    return directories


# In[2]:

def print_help() :
        print("list of all commands:")
        print("  l - list all docs")
        print("  f <document number> - show name in the doc")
        print("  s <document number> - show directory where is the doc")
        print("  a - add new document")
        print("  d <document number> - delete doc")
        print("  m <document number> - move doc from the one dir to another")
        print("  xl - list of all directories")
        print("  xs <dir number> - show all docs in the dir")
        print("  xa <dir number> - add new dir")
        print("  xd <dir number> - delete dir")
        print("  e, ex, exit - exit program")
        print("  h, he, help - show all commands")


# In[6]:

def print_dir_with_doc(num, adir) :
    for d in adir.items():
        if num in d[1] :
            print(d)


# In[3]:

def get_command() :
    while True:
        c = input("Enter command (h - help, ex - exit):").lower().split()
        if (len(c) > 0) :
            return c


# In[4]:

def l_com(adocs, adir):
    for i,d in enumerate(adocs ) :
        print(i+1,d)


# In[9]:

def find_dir_by_num(num, adir) :
    for d in adir.items():
        if num in d[1] :
            return d[0]
    print('error: document '+num + ' was not found in all directories')


# In[5]:

def f_com(num, adocs, adir):
    for d in adocs :
        if d['number'] == num :
            print(d)
            return
    print("no document with number " + num)


# In[7]:

def s_com(num, adocs, adir):
    for d in adocs :
        if d['number'] == num :
            print_dir_with_doc(num, adir)
            return
    print("no document with number " + num)


# In[8]:

def d_com(num, adocs, adir):
    for d in adocs :
        if d['number'] == num :
            print("document " + str(d) + " deleted")
            adocs.remove(d)
            return
    print("no document with number " + num)


# In[10]:

def m_com(num, adocs, adir):
    for d in adocs :
        if d['number'] == num :
            old_dir = find_dir_by_num(num, adir)
            while True:
                new_dir = input("document found in the dir #"+old_dir[0]+" enter new dir number:")
                if new_dir in adir.keys() :
                    adir.get(old_dir).remove(num)
                    adir.get(new_dir).append(num)
                    print("document moved to the dir #"+new_dir)
                    break
                else:
                    print("wrong dir number")
            return
    print("no document with number " + num)


# In[34]:

def xl_com(adocs, adir):
    for d in adir.items() :
        print(d)


# In[49]:

def xs_com(num, adocs, adir):
    if num in adir.keys():
        print (num + " " + str(adir.get(num)) )
        return
    else :
        print("no directory with number " + num)

def no_invalid_chars(line) :
    if set('[~!@#$%^&*()_+{}":;\']+$ ').intersection(line):
        return False
    else :
        return True

def a_com(adocs, adir):
    while True:
        dtype = input("enter document type:")
        if dtype.isalpha() :
            break
        else:
            print ("invalid character in the doc type")
    while True:
        dnum = input("enter document number:")
        if no_invalid_chars(dnum) :
            break
        else:
            print ("invalid character in the doc number")
    while True:
        dname = input("enter document name:")
        if all(x.isalpha() or x.isspace() for x in dname) :
            break
        else:
            print ("invalid character in the doc name")
    while True:
        d_dir = input("enter document directory:")
        if d_dir in adir.keys() :
            break
        else:
            print ("wrong directory number: available numbers are: " + str(adir.keys() ))
    
    adocs.append( {"type":dtype, "number":dnum, "name":dname} )
    d_list = adir.get(d_dir)
    d_list.append(dnum)
    adir[d_dir] = d_list
    print("document type: "+dtype+" number: "+dnum+" name: "+dname+ " added to the dir #"+d_dir)

def xd_com(d_dir, adocs, adir):
    if d_dir in adir.keys() :
        d_list = adir.get(d_dir)
        if not len(d_list) :
            del adir[d_dir]
            print("directory #"+d_dir+" deleted")
        else:
            print ("directory has documents in it,  please move all docs to another dir first!")  
    else:
        print ("wrong directory number, valid dir numbers are: " + ", ".join(list(adir.keys())) )  

def xa_com(adocs, adir):
    for i in range(1,1000):
        if (str(i) not in adir.keys()):
            t = list()
            adir[str(i)] = t
            print ("directory #"+str(i)+" was created")
            return
    print("programm has reached maximum number 1000 of directories")

def main() :
    possibles = globals().copy()
    possibles.update(locals())
    all_docs = get_all_documents()
    all_dir = get_all_directories()
    c_list = { "l":1, "f":2, "s":2, "d":2, "m":2, "xl":1, "xs":2, "a":1, "xd":2, "xa":1 }
    print("Program started, data loaded\n")
    
    while True:
        c = get_command()
        if c[0] in ["ex", "e", "exi", "exit"] :
            break
        if c[0] in ["h", "he", "hel", "help"] :
            print_help()
            continue
        if (len(c)) > 2 :
            print("error: too many parameters")
            continue
        if c[0] in c_list :
            func = possibles.get(c[0]+"_com")
            
            if (len(c) == 1) and (c_list.get(c[0]) == 1):
                func(all_docs, all_dir)
            elif (len(c) == 2) and (c_list.get(c[0]) == 2) :
                func(c[1], all_docs, all_dir)
            else:
                print("error: wrong number of parameters")
        else :
            print("wrong command, for help type - h")
        
    print("\n\nProgram stopped, data saved")

if __name__ == "__main__":
    main()


# In[ ]:



