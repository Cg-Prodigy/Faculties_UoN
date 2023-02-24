import requests
import json
import time
from bs4 import BeautifulSoup
from pprint import pprint
import os
if os.stat("faculties.json").st_size ==0:
    url="https://www.uonbi.ac.ke/faculties-departments"
    client=requests.get(url).content

    html=BeautifulSoup(client, "html.parser")
    parent=html.find("table")
    table_row=parent.find_all("tr")
    department=[]
    links=[]
    for each in table_row:
        p=None
        td=each.find_all("td")
        for each in td[1].find_all("p"):
            p=each.find("strong").text
        for each in td[-1].find_all("ol"):
            obj={}
            obj[p]=[]
            d_a={}
            for li in each.find_all("li"):
                a=li.find("a")["href"]
                d=li.text.strip(" ").strip("\u00a0")
                obj[p].append({d:a})
                d_a[d]=a
            links.append(d_a)
            department.append(obj)
    with open("faculties.json","w") as file:
        json.dump(department,file)   
    with open("links.json","w") as file:
        json.dump(links,file)
else:
    start_time=time.perf_counter_ns()
    end_time=None
    courses=[]
    with open("links.json", "r") as file:
        data=json.loads(file.readline())
        for each in data:
            obj={}
            for key in each.keys():
                url=each[key]
                client=requests.get(url).content
                bs4_inner=BeautifulSoup(client,"html.parser")
                try:
                    root=bs4_inner.find("div",class_="view-mt-courses")
                    root_two=root.find("div",class_="more-link")
                    link=root_two.find("a")["href"]
                    new_url=url[:-1]+link if url.endswith("/") else url+link
                    print(new_url,link)
                    client_two=requests.get(new_url).content
                    bs4_scholar=BeautifulSoup(client_two,"html.parser")
                    root_two=bs4_scholar.find("div",id="block-scholarly-content")
                    all_views=root_two.find_all("div",class_="views-row")
                    lst=[]
                    for view in all_views:
                        div=view.find("div",class_="views-field-title")
                        course=div.find("span").text
                        lst.append(course)
                    obj[key]=lst
                except Exception as e:
                    print(e)
                    obj[key]=[]
            print(obj)
            courses.append(obj)
        end_time=time.perf_counter_ns()
    print(start_time-end_time)
    with open("courses.json", "w") as file:
        json.dump(courses,file)
                    