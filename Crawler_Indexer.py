import urllib2
import os

#crawling

def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return None

def get_page_ex(fil):
    try:
        f=open(fil,'r')
        return f.read()
    except:
        return None
    

def get_next_target(page):
    start_link=page.find('<a href')
    start_quote=page.find("'",start_link)
    end_quote=page.find("'",start_quote+1)
    url=page[start_quote+1:end_quote]
    return url,end_quote

def get_all_links(page):
    links=[]
    while True:
        url,endpos=get_next_target(page)
        if url:
            links.append(url)
            page=page[endpos:]
        else:
            break
    return links

def crawl_web(seed):
    tocrawl=[seed]
    crawled=[]
    ind=[]
    index={}
    graph={}
    while tocrawl:
        page=tocrawl.pop()
        if page not in crawled:
            foo=get_page_ex(page)
            if foo is None:
                continue
            add_page_to_index(index,page,foo)
            ind=get_all_links(foo)
            graph[page]=ind
            for i in ind:
                tocrawl.append(i)
            crawled.append(page)
    for p in index:
        index[p]=list(set(index[p]))
    pickle.dump(index,open('Data/engine_data.p','wb'))
    return crawled,index,graph


def html_elements(content):
    a=''
    check=1
    for i in content:
        if i=='<':
            check=0
        if check:
           a=a+i
        if i=='>':
            check=1
    return a



#indexing

def add_page_to_index(index,url,content):
    contentx=html_elements(content)
    words=contentx.split()
    for word in words:
        index=add_to_index_dictionary(index,word,url)
 
    
def add_to_index_dictionary(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword]=[url]
    return index


def compute_ranks(graph):
    d=0.8
    numloops=10
    ranks={}
    npages=len(graph)
    for page in graph:
        ranks[page]=1.0/npages
    for i in range(0,numloops):
        newranks={}
	print graph
        for page in graph:
            newrank=(1-d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank=newrank+d*(ranks[node]/len(graph[node]))
           	newranks[page]=newrank
        ranks=newranks
    pickle.dump(ranks,open('Data/data_files/page_ranks.p','wb'))
    return ranks


#dummy   


import pickle
a,b,c=crawl_web('Data/airports/mumbai.html')

