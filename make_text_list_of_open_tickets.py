import cPickle as pickle

from sys import platform as _platform

import os

from tabulate import tabulate

new_responsible_author = 'icaoberg'

try:
	username = os.environ['USER']
except:
	username = 'unknown'

def banner(text, ch='=', length=50):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    return banner

if _platform == "linux" or _platform == "linux2":
    computer = 'lanec1.compbio.cs.cmu.edu'
elif _platform == "darwin":
    computer = 'woodstock.compbio.cs.cmu.edu'
elif _platform == "win32":
    computer = 'jabberwocky.compbio.cs.cmu.edu'

print "This is an automated report from " + username + "@" + computer + "."

comment = '''
This script generates a list of useful information for developers of CellOrganizer.
'''

print comment

print "\nConnecting to bitbucket.org"
execfile( 'bitbucket_connect.py' )

[success, issues] = bb.issue.all()
number_of_issues = issues['count']

print "Getting repository: " + username + "@" + slug + "\n"
[anwser, repo] = bb.repository.get( slug )

kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

list_of_issues = []
print "Number of issues found: " + str(number_of_issues)
print "Retrieving issues one by one"
for issue_number in range( number_of_issues, 1, -1  ):
	[answer, issue] = bb.issue.get( issue_number )
	list_of_issues.append( issue )

title = "List Open/New Issues per Author"
kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

print banner( title.upper() )
list_of_issues_per_user = {}
for issue in list_of_issues:
	try:
		if issue.has_key( 'responsible' ):
			responsible = issue['responsible']['username']
		else:
			responsible = 'unknown'
		responsible = responsible.encode('ascii','ignore')

		if issue['status'] in status:
			if list_of_issues_per_user.has_key( responsible ):
				if issue['metadata']['kind'] == 'bug':
					list_of_issues_per_user[ responsible ] = map(sum, zip(list_of_issues_per_user[ responsible ],[1,0,0,0]))
				elif issue['metadata']['kind'] == 'enhancement':
					list_of_issues_per_user[ responsible ] = map(sum, zip(list_of_issues_per_user[ responsible ],[0,1,0,0]))
				elif issue['metadata']['kind'] == 'proposal':
					list_of_issues_per_user[ responsible ] = map(sum, zip(list_of_issues_per_user[ responsible ],[0,0,1,0]))
				else:
					list_of_issues_per_user[ responsible ] = map(sum, zip(list_of_issues_per_user[ responsible ],[0,0,0,1]))
			else:
				list_of_issues_per_user[ responsible ] = [0,0,0,0]
	except:
		print ""

headers = ['AUTHOR']
headers.extend(  [x.upper() for x in kind] )
headers.extend( ['URL'] )

data = []
for author in list_of_issues_per_user:
	datum = [ author ]
	datum.extend( list_of_issues_per_user[ author ] )
	datum.extend( ['https://bitbucket.org/icaoberg/cellorganizer/issues?responsible=' + author])
	data.append( datum )

print tabulate( data, headers, tablefmt="grid" )
print ""

title = "Summary Open/New Issues per Version"
kind = {'bug', 'task'}
status = {'new', 'open'}
print banner( title.upper() )
print "URL: https://bitbucket.org/icaoberg/cellorganizer/issues?kind=task&kind=bug&status=open&status=new"
list_of_issues_per_version = {}
for issue in list_of_issues:
	try:
		if issue['status'] in status:
			if issue['metadata']['kind'] in kind:
				version = issue['metadata']['version']

				try:
					version = version.encode('ascii','ignore')
				except:
					version = 'None'

				if not list_of_issues_per_version.has_key( version ):
					list_of_issues_per_version[ version ] = 0;
				else:
					list_of_issues_per_version[ version ] = list_of_issues_per_version[ version ] + 1
	except:
		print ""

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

print tabulate( data, headers, tablefmt="grid" )
print ""

title = "Summary all Issues per Version"
print banner( title.upper() )
print "URL: https://bitbucket.org/icaoberg/cellorganizer/issues?status=new&status=open"

kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}
list_of_issues_per_version = {}
for issue in list_of_issues:
	try:
		if issue['status'] in status:
			version = issue['metadata']['version']

			try:
				version = version.encode('ascii','ignore')
			except:
				version = 'None'

			if not list_of_issues_per_version.has_key( version ):
				list_of_issues_per_version[ version ] = 0;
			else:
				list_of_issues_per_version[ version ] = list_of_issues_per_version[ version ] + 1
	except:
		print ""

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

print tabulate( data, headers, tablefmt="grid" )
print ""

title = "Summary of all open issues"
print banner( title.upper() )
data = []
headers = ["ID", 'VER', 'TITLE', 'RESPONSIBLE', 'URL']
for issue in list_of_issues:
	try:
		if issue['status'] in status:
			if issue.has_key( 'title' ):
				title = issue['title']
				title = title[:75] + (title[75:] and '..')
			else:
				title = 'Title not set'

			if issue.has_key( 'responsible' ):
				responsible = issue['responsible']['username']
			else:
				responsible = 'Unknown'

			version = issue['metadata']['version']
			if not version:
				version = 'Unassigned'

			url = 'https://bitbucket.org/icaoberg/cellorganizer/issue/' + str(issue['local_id'])

			datum = [issue['local_id'], version, title, responsible, url]
			data.append( datum  )
	except:
		print ""

print tabulate( data, headers, tablefmt="grid" )
print ""
