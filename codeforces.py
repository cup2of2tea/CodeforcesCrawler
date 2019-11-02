import requests
from bs4 import BeautifulSoup
import os
import sys, traceback
from selenium import webdriver
import time
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(chrome_options=options)

pseudo = 'cup_of_tea'
sortie = 'C:/Users/Megaport/projects/CompetitiveProgramming/codeforces'

ids = []

browser.get('https://codeforces.com/submissions/'+pseudo)
soup = BeautifulSoup(browser.page_source,features="html.parser")

lastPage = int(soup.find_all(lambda tag: tag.name == 'span' and 'pageindex' in tag.attrs)[-1].attrs['pageindex'])
print(lastPage)

reqSubmission = None
for p in range(1,lastPage+1):
    try:
        req = browser.get('https://codeforces.com/submissions/'+pseudo+'/page/'+str(p))
        soup = BeautifulSoup(browser.page_source,features="html.parser")

        links = soup.find_all(lambda tag: tag.name=='tr' and 'data-submission-id' in tag.attrs
                              and tag.findChild(lambda tag: tag.name=='span' and 'submissionverdict' in tag.attrs and tag.attrs['submissionverdict'] == 'OK'))

        for link in links:
            time.sleep(10)
            try:
                aLink = link.find(lambda tag: tag.name=='a' and 'href' in tag.attrs and '/submission/' in tag.attrs['href'])
                print(aLink.attrs['href'])
                browser.get('https://codeforces.com' + aLink.attrs['href'])

                soupSubmission = BeautifulSoup(browser.page_source, features="html.parser")
                rawCode = '\n'.join(map(lambda line: line.text,soupSubmission.find('pre',{'id':'program-source-text'}).find_all('li')))
                problemLink = soupSubmission.find(lambda tag: tag.name == 'a' and 'href' in tag.attrs\
                                                              and '/problem/' in tag.attrs['href'] and '/contest/' in tag.attrs['href'])
                idProblem = problemLink.attrs['href']
                if(idProblem in ids):
                    continue
                ids.append(idProblem)
                reqProblem = browser.get('https://codeforces.com' + problemLink.attrs['href'])
                soupProblem = BeautifulSoup(browser.page_source,features="html.parser")
                title = soupProblem.find('div', {'class':'problem-statement'})\
                                    .find('div', {'class':'title'})\
                                    .text;
                contestTitle = soupProblem.find(lambda tag: tag.name == 'a' and 'href' in tag.attrs and '/contest/' in tag.attrs['href'])\
                                            .text;

                title = title.replace('.','_').replace(' ','_').replace('__','_').replace(':','_')
                contestTitle = contestTitle.replace('.','_').replace(' ','_').replace('__','_').replace(':','_')

                print(title)
                print(contestTitle)

                os.makedirs(sortie+'/'+contestTitle,exist_ok=True)
                with open(sortie+'/'+contestTitle+'/'+title+'.cpp','w') as f:
                    f.write(rawCode)

            except:
                traceback.print_exc(file=sys.stdout)
                pass

    except:
        traceback.print_exc(file=sys.stdout)
        pass