from bs4 import BeautifulSoup #install
import requests #install
from os import getcwd

def download_dir_lists(): #Downloads the directory name list to search for inside the website
    dirlisturl = "https://raw.githubusercontent.com/the-xentropy/samlists/refs/heads/main/sam-gh-directories-lowercase-top1000.txt"
    dirlistraw = requests.get(dirlisturl)
    open(getcwd()+ "/dirlistfile.txt" , 'wt').write(dirlistraw.text.strip())
    dirlistfile = open(getcwd()+ "/dirlistfile.txt" , 'rt')
    dirlist1 = dirlistfile.readlines()
    dirlist = []
    for n in dirlist1:
        dirlist.append(n.strip("\n"))
    return dirlist

# def testWebsite(target):
#     response = requests.get("http://" + target)
#     if response.status_code == 200:
#         target = "http://"+target
#     elif response.status_code != 200:
#         print("No response for HTTP.\nTrying HTTPS:")
#         response = requests.get("https://" + target)
#         if response.status_code == 200:
#             print("Target is working in HTTPS.")
#             target = "https://"+target
#     return target

def dir_search(dir, dirlist): #Creates a list of the website directories as links
    dirlist = dirlist[0:9]
    print("[*] Website " + dir + " found\n[*] Starting dir search:")
    for n in dirlist:
        gettest = requests.get(dir + "/" +n)
        print("testing: " + dir + "/" +n)
        if gettest.status_code == 200:
            websitedirs.append(dir + "/" +n)
            print("found: " + dir + "/" +n)
    print("[*] Found the following directories: " + str(websitedirs))
    return websitedirs

def remove_duplicates(list): #Removes duplicates from a list
    newlist=[]
    seen = set()
    for item in list:
        if item not in seen:
            newlist.append(item)
            seen.add(item)
    return newlist

def link_extractor(target): # function to extract links in website html
    print("Extracting links for: " + target)
    websitelinks = []
    targethtml = requests.get(target)
    soup = BeautifulSoup(targethtml.text, "html.parser")
    print('[*] For directory ' + target + ' links are:')
    links = soup.find_all('a')
    for link in links:
        link = link.get('href')
        strippedlink = link.lstrip('/')
        if 'toscrape.com' in strippedlink:
            websitelinks.append(strippedlink)
        else:
            websitelinks.append(target + link)
    websitelinks = remove_duplicates(websitelinks)
    print(websitelinks)
    return websitelinks

def files_to_download(tag_list,file_extensions_tuple, websitedirs):
    downloadable = []
    for url in websitedirs:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in tag_list:
            if tag == 'a':
                for element in soup.find_all(tag):
                    value = element.get('href')
                    if value and value.endswith(file_extensions_tuple):
                        downloadable.append(url + value)
            else:
                for element in soup.find_all(tag):
                    value = element.get('src')
                    if value and value.endswith(file_extensions_tuple):
                        downloadable.append(url + value)
    print("downloadable links: \n" + str(downloadable))
    return downloadable
# !!! Defying basic variables !!!
target = input("Please enter full website address (http://www.example.com): ")
# target = "http://toscrape.com"
response = requests.get(target)
dirlist = download_dir_lists()
response = requests.get(target , timeout= 5)
websitehtml = requests.get(target).text #saves the websites html as value
websitedirs = [target] # list filled by dirSearch containing all directories found by dirSearch
websitelinks = [] #list filled by link extractor



# !!! Directories searching !!!
if response.status_code == 200: # Checks if website exists ##might turn into function
    print("[*] Target is Alive!")
    websitedirs = dir_search(target, dirlist)
    for dir in websitedirs: #Extracting links from targets
        websitelinks.append(link_extractor(dir))
elif response.status_code != 200:
    print("No response for HTTP.\nTrying HTTPS:")
    target = target.replace('http' , 'https')
    response = requests.get(target)
    if response.status_code == 200:
        print("Target is working in HTTPS.")
        websitedirs = dir_search(target, dirlist)
        for dir in websitedirs: #Extracting links from targets
            websitelinks.append(link_extractor(dir))
    else:
        print("Target is not available")




print("These are all the links on the sitemap: " + str(websitelinks))

# !!! Creating downloadable files list !!!
tag_list = ['a', 'audio', 'video', 'img', 'image']
file_extensions_tuple = ('.mp3' , '.mp4', '.pdf', '.png', '.jpg', '.gif')
files_to_download(tag_list,file_extensions_tuple, websitedirs) # Creates a list of files to download - can be used later to download.
