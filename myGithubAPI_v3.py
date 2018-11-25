# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:54:45 2018

@author: zack
"""

from github import Github
import pandas as pd  #Use pandas.DataFrame.to_csv func to get a csv file


#Enter your Github username and password
user = '*******'  #Replace it
password = '******'  #Replace it
g = Github(user,password)

#calling the search repo API
def get_repositories(keywords):
    
    repositories = g.search_repositories(query = keywords)
    print('get repositories {}'.format(repositories.totalCount))
    
    return repositories


def get_issueInfo(repo_issues,repo_name,repo_owner):
    ''' Get the issues information list.
    
    Retrieves information list of issue which belong to the given repository.
    
    Args:
        repo_issues: A issue list of the given repo, obtained by repo.get_issues().
        repo_name: a name of the given repo.
        repo_owner: a name of the owner of the given repo.
        
    Return:
        issue_info_list: A issue imformation list of the given repo.

    '''
    issue_info_list = []
    for issue in repo_issues:
        issue_id = issue.id
        issue_state = issue.state
        issue_state.encode('utf-8','ignore')
        issue_title = issue.title
        issue_title.encode('utf-8','ignore')
        issue_label = ''
 #some issues do not have label and body
        if issue.labels != None :
            for label in issue.labels:
                issue_label = label.name
                issue_label.encode('utf-8','ignore')
        issue_html_url = issue.html_url
        issue_html_url.encode('utf-8','ignore')
        issue_body = issue.body
        if issue_body != None:
            issue_body.encode('utf-8','ignore') 
        issue_info_list.append([repo_name,repo_owner,issue_id,issue_title,issue_state,
                                issue_label,issue_html_url,issue_body])
    
    return issue_info_list
    


if __name__ == '__main__':
    keywords = input('Enter your keywords:')
    repositories = get_repositories(keywords)
    for repo in repositories:
        repo_name = repo.name
        repo_name.encode('utf-8','ignore')
        print(repo_name)
        repo_owner = repo.owner.login
        repo_owner.encode('utf-8','ignore')
        repo_issues = repo.get_issues()
        issue_info_list = []
        issue_info_list = get_issueInfo(repo_issues,repo_name,repo_owner)
#some repos do not have issue
        if len(issue_info_list) == 0:
            continue
        flag = 1
        fileName = 'issues_of_'+ keywords + '.csv'
        data = pd.DataFrame(issue_info_list)
        try:
            if flag == 1:
                csv_headers = ['repo_name','repo_owner','issue_id','issue_title','issue_state',
                                'issue_label','issue_html_url','issue_body']
                data.to_csv(fileName, header = csv_headers, index = False, 
                            mode = 'a+', encoding = 'utf-8-sig')

            else:
                data.to_csv(fileName,header = False, index = False,
                            mode = 'a+', encoding = 'utf-8-sig')
                flag += 1
        except UnicodeEncodeError:
            print('Encode error drop the data')