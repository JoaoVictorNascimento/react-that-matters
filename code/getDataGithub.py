# -*- coding: utf-8 -*-
from github import Github
import json
import time
import moment
from datetime import datetime
import csv
from tokens import tokens
import pandas as pd

# Global variables

repository_name = ''  # owner and repo name

data = {
    "repositories": []
}

token_index = 0
api = Github(tokens[token_index])

issue_number = 0
repository = None

# Methods

def countRequest():
    print(api.rate_limiting[0])

def treat_requests_number():
    global token_index
    global api
    global tokens
    global repository_name
    global repository
    
    if (api.rate_limiting[0] <= 20):
        token_index += 1
        if(token_index == len(tokens)):
            token_index = 0
        api = Github(tokens[token_index])
        repository = api.get_repo(repository_name)
    
def writeFile(data):
    with open('../data/dataGithub.json', 'w') as outfile:
        json.dump(data, outfile)

def get_n_issues():
    treat_requests_number()
    n_issues = repository.get_issues(state="all").totalCount
    return n_issues

def get_n_comment_issues():
    treat_requests_number()
    n_comment_issues = repository.get_issues_comments().totalCount
    return n_comment_issues

def get_n_issues_closed():
    treat_requests_number()
    n_issues_closed = repository.get_issues(state="closed").totalCount
    return n_issues_closed

def get_n_issues_open():
    treat_requests_number()
    n_issues_open = repository.get_issues(state="open").totalCount
    return n_issues_open

def get_n_releases():
    treat_requests_number()
    n_releases = repository.get_releases().totalCount
    return n_releases

def get_statistical_time(initialKey, FinalKey):    
    global issue_number
    items_formatted = []
    
    while(issue_number > -1):
        try:
            issue = repository.get_issue(issue_number)
            treat_requests_number()
            print(issue)
            print(issue_number)
            
            if issue.raw_data[initialKey] and issue.raw_data[FinalKey]:
                time.sleep(1.1)
                createdTime = moment.date(issue.raw_data[initialKey])
                closedTime = moment.date(issue.raw_data[FinalKey])
                items_formatted.append({initialKey: createdTime, FinalKey: closedTime})
            issue_number -= 1
        except:
            issue_number -= 1
            continue
            
        
    dataFrame = pd.DataFrame(items_formatted, columns=[initialKey, FinalKey])
    diff_time = dataFrame[FinalKey] - dataFrame[initialKey]
    diff_average_time = diff_time.mean()
    max_time = diff_time.max()
    min_time = diff_time.min()
    normalized_diff_time = (diff_time - min_time)/(max_time - min_time)
    normalized_average_time = normalized_diff_time.mean()
    
    return max_time, diff_average_time, normalized_average_time
    
def get_labels():
    treat_requests_number()
    labels = repository.get_labels()
    if labels.totalCount == 0 : return None
 
    labelsData = []
    
    for label in labels:
        treat_requests_number()
        try:
            labelsData.append(label.raw_data['name'])
        except:
            continue
    
    return labelsData

def get_license():
    treat_requests_number()
    license = None
    try:
        license = repository.get_license()
        return license.raw_data['license']['name']
    
    except:
        return license
     
def get_basicData():
    dataRepository = {
        repository_name : {}
    }
    
    global issue_number
    
    treat_requests_number()
    
    issue_number = repository.get_issues(state="closed")[0].number
    print('Total Issues: ', issue_number)
    max_time_issue_open, average_time_issue_open, normalized_average_time_open = get_statistical_time('created_at', 'closed_at')
    last_version_release = ""
    last_published_at = ""
    
    try:
        last_release = repository.get_latest_release()
        last_version_release = last_release.raw_data['tag_name']
        last_published_at = last_release.raw_data['published_at']
    except:
        print("No have release")

    dataRepository[repository_name] = {
        'language': repository.language,
        'created_at': str(moment.utc(repository.created_at).date),
        'updated_at': str(moment.utc(repository.updated_at).date),
        'pushed_at': str(moment.utc(repository.pushed_at).date),
        'open_issues': repository.open_issues,
        'forks_count': repository.forks_count,
        'description': repository.description,
        'size': repository.size,
        'stargazers_count': repository.stargazers_count,
        'subscribers_count': repository.subscribers_count,
        'watchers': repository.watchers,
        "issues_closed": get_n_issues_closed(),
        "max_time_issue_open": str(max_time_issue_open),
        "average_time_issue_open": str(average_time_issue_open),
        "normalized_average_time_open": normalized_average_time_open,
        "comments_issues": get_n_comment_issues(),
        "labels": get_labels(),
        "license": get_license(),
        "releases_count": get_n_releases(),
        "last_version_release": last_version_release,
        "last_published_at": last_published_at,
    }
    
    data['repositories'].append(dataRepository)
    writeFile(data)
     
def get_data():
    get_basicData()
    
def writeRowCSV(repository):
    nameRepository = ''
    for key in repository.keys():
        nameRepository = key
            
    dataArray = [nameRepository, repository[nameRepository]['language'], repository[nameRepository]['created_at'], 
                 repository[nameRepository]['updated_at'], repository[nameRepository]['pushed_at'], repository[nameRepository]['open_issues'],
                 repository[nameRepository]['forks_count'], repository[nameRepository]['description'], repository[nameRepository]['size'],
                 repository[nameRepository]['stargazers_count'], repository[nameRepository]['subscribers_count'],
                 repository[nameRepository]['watchers'], repository[nameRepository]['issues_closed'],
                 repository[nameRepository]['max_time_issue_open'], repository[nameRepository]['average_time_issue_open'],
                 repository[nameRepository]['normalized_average_time_open'], repository[nameRepository]['comments_issues'],
                 repository[nameRepository]['labels'], repository[nameRepository]['license'], repository[nameRepository]['releases_count'],
                 repository[nameRepository]['last_version_release'], repository[nameRepository]['last_published_at']]
    
    return dataArray
    
def convertToCSV():
    with open('../data/dataGithub.json') as jsonFile:
        data = json.load(jsonFile)
        
        with open('../data/data.csv', 'w', newline='') as csvFile:
            fieldNames = ['name', 'language', 'created_at', 'updated_at', 'pushed_at', 
                          'open_issues', 'forks_count', 'description', 'size', 'stargazers_count', 
                          'subscribers_count', 'watchers', 'issues_closed', 'max_time_issue_open',
                          'average_time_issue_open', 'normalized_average_time_open', 'comments_issues',
                          'labels', 'license', 'releases_count', 'last_version_release', 'last_published_at']
            writer = csv.writer(csvFile)
            writer.writerow(fieldNames)
            
            for repository in data['repositories']:
                writer.writerow(writeRowCSV(repository))

        
        

def main():
    file = open('inputFile.txt', 'r')
    lines = file.read().splitlines()
    
    for line in lines:
        global repository_name
        global repository
        repository_name = line
        treat_requests_number()
        
        print(repository_name)
        repository = api.get_repo(repository_name)
        get_data()
    convertToCSV()
                
main()
    