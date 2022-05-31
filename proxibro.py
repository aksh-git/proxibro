import requests
import time
import os
import shutil
from fake_headers import Headers
import concurrent.futures.thread
from concurrent.futures import ThreadPoolExecutor, as_completed

proxyAPI = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=all&timeout=10000&country=all&ssl=all&anonymity=all"
doFilter = ""
checked = {}
threads = 200
proxyFile = ""
sortByType = True
fileNames = ("http-proxibro.txt","socks4-proxibro.txt","socks5-proxibro.txt")

def fileHandler(file):
    findex = file.index("-")
    filetype = file[:findex]
    if file not in fileNames:
        pass
    else:
        if (not os.path.isfile(file)):
            pass
        else:
            print(open(file).read(), file=open(filetype+'Backup.txt', 'a'))
            os.remove(file)
            print("\tBackuped :",file)

def banner():
    print("""      

    ██████╗░██████╗░░█████╗░██╗░░██╗██╗██████╗░██████╗░░█████╗░
    ██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝██████╔╝██║░░██║░╚███╔╝░██║██████╦╝██████╔╝██║░░██║
    ██╔═══╝░██╔══██╗██║░░██║░██╔██╗░██║██╔══██╗██╔══██╗██║░░██║
    ██║░░░░░██║░░██║╚█████╔╝██╔╝╚██╗██║██████╦╝██║░░██║╚█████╔╝
    ╚═╝░░░░░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝░╚════╝░
                                         written by : aksh-git 
    -----------------------------------------------------------
    """)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        #Author : aksh-git
def getProxy():
    try:
        header = Headers(
            headers=False
        ).generate()
        agent = header['User-Agent']
        headers = {
            'User-Agent': f'{agent}',
        }
        response = requests.get(proxyAPI, allow_redirects=True)
        status = response.status_code
        if status != 200:
            raise Exception
        else:
            global proxyFile
            proxyFile = "NewProxibro-"+str(int(round(time.time() * 1000)))+".txt"
            f = open(proxyFile, "wb")
            f.write(response.content)
            f.close()
            print("\tFresh Proxies Has been loaded Successfully.")
    except Exception as e:
        print("ERROR : ",e)
        pass

def load_proxy():
    proxies = []
    try:
        if os.path.isfile('GoodProxy.txt'):
            shutil.copy('GoodProxy.txt', 'ProxyBackup.txt')
            print("\n\t    GoodProxy backed up in ProxyBackup File..")
            os.remove('GoodProxy.txt')
        if proxyFile=="GoodProxy.txt":
            exit(0)
    except Exception as e:
        print("Error : ",e)

    load = open(proxyFile)
    loaded = [items.rstrip().strip() for items in load]
    load.close()

    for lines in loaded:
        if lines.count(':') == 3:
            split = lines.split(':')
            lines = f'{split[2]}:{split[-1]}@{split[0]}:{split[1]}'
        proxies.append(lines)

    return proxies

def mainChecker(proxy_type, proxy, position):

    checked[position] = None

    proxyDict = {
        "http": f"{proxy_type}://{proxy}",
        "https": f"{proxy_type}://{proxy}",
    }

    try:
        header = Headers(
            headers=False
        ).generate()
        agent = header['User-Agent']

        headers = {
            'User-Agent': f'{agent}',
        }

        response = requests.get(
            'https://www.google.com/', headers=headers, proxies=proxyDict, timeout=15)
        status = response.status_code

        if status != 200:
            raise Exception

        print( f"Tried {position+1} |" f' {proxy} | GOOD | Type : {proxy_type} | Response : {status}')

        if(sortByType):
            print(proxy, file=open(proxy_type+'-proxibro.txt', 'a'))
        else:
            print(proxy, file=open('GoodProxy.txt', 'a'))
    except:
        print(f"Tried {position+1} |" f' {proxy} | {proxy_type} | BAD ')
        checked[position] = proxy_type
        pass

def proxyCheck(position):
    proxy = proxy_list[position]
    mainChecker('http', proxy, position)
    if checked[position] == 'http':
        mainChecker('socks4', proxy, position)
    if checked[position] == 'socks4':
        mainChecker('socks5', proxy, position)

def filterProxy():
    pool_number = [i for i in range(total_proxies)]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(proxyCheck, position)
                   for position in pool_number]
        try:
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
        except IndexError:
            print('Number of proxies are less than threads. Provide more proxies or less threads.')
            pass

def startFilter():
    for file in fileNames:
        fileHandler(file)
    global proxy_list
    proxy_list = load_proxy()
    print("\n\tRemoving duplicate proxies...")
    time.sleep(1)
    proxy_list = list(set(proxy_list))  # removing duplicate proxies
    print("\t\tRemoving Empty proxies...")
    time.sleep(1)
    proxy_list = list(filter(None, proxy_list))  # removing empty proxies
    global total_proxies
    total_proxies = len(proxy_list)
    print(f'Total proxies : {total_proxies}')
    filterProxy()

def proxy():
    print("   [Note : Filtering process takes some time ,\n    but it is advised to use filter for best results ]")
    doFilter = str(input("\n    Want Filtered proxy [y/n] : "))
    if doFilter=="y" or doFilter=="yes" or doFilter=="Y":
        print("    Getting Fresh Proxies...")
        time.sleep(2)
        getProxy()
        print("\tFiltering Proxies...")
        time.sleep(2)
        startFilter()
        time.sleep(1)
        print("\n    All proxies has been filtered.")
        time.sleep(1)
        print("\tGood Proxies has been saved to a txt file acc. to their type.")
        time.sleep(1)
        print("\t    Removing bad proxies...")
        try:
            time.sleep(1)
            os.remove(proxyFile)
            print("\n\tBad Proxies had been removed Successfully.")
        except Exception as e:
            print("Error : ",e)
    else:
        print("\n    Getting Fresh Proxies...")
        time.sleep(2)
        getProxy()
    time.sleep(1)
    print("\n\t<=[ Thank You for using this. ]=>")

if __name__=="__main__":
    os.system("")
    banner()
    print("    [Options]")
    print("    [1] Get Fresh Proxies : ")
    print("    [2] Check Proxy Status From A File : ")
    choice = int(input("\n    Want's to go with : "))
    if choice==1:
        try:
            proxy()
        except Exception as e:
            print("\n\tError : ",e)
    elif choice==2:
        proxyFile = str(input("\n\tEnter Your File Name/Path : "))
        try:
            startFilter()
            print("\n\tAll proxies has been filtered.")
        except Exception as e:
            print("\n\tError : ",e)
    else:
        print("\n\tNO OPTIONS LIKE THIS")
        print("\n\tWant some new feature..!? kindly let me know your idea..\n\ttext me here on telegram : t.me/aksh-git")
