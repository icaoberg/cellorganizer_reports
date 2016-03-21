import cPickle as pickle

from sys import platform as _platform
import datetime
import collections
from operator import itemgetter

import os

from tabulate import tabulate

tabulate_output_format = 'html'

if tabulate_output_format == 'html':
	output_filename = 'daily_report-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
	if os.path.isfile( output_filename ):
		os.remove( output_filename )
	output_fileID = open( output_filename, 'w' )
else:
	output_filename = 'daily_report-' + datetime.datetime.now().strftime('%Y-%m-%d') + '.txt'

new_responsible_author = 'icaoberg'

try:
	username = os.environ['USER']
except:
	username = 'unknown'

def banner(text, ch='=', length=100):
    spaced_text = ' %s ' % text
    banner = spaced_text.center(length, ch)
    return banner

if _platform == 'linux' or _platform == 'linux2':
    computer = 'lanec1.compbio.cs.cmu.edu'
elif _platform == 'darwin':
    computer = 'woodstock.compbio.cs.cmu.edu'
elif _platform == 'win32':
    computer = 'jabberwocky.compbio.cs.cmu.edu'

################################################################################
message = '''
<h1>CellOrganizer Daily Report</h1>
<ul>
<li><a href='#jenkins'>CellOrganizer CI Daily Report</a></li>
<li><a href='#repository'>CellOrganizer Repository Daily Report</a></li>
<li><a href='#python'>CellOrganizer for Python Daily Report</a></li>
<li><a href='#documentation'>CellOrganizer Documentation Daily Report</a></li>
</ul>
'''
if tabulate_output_format == 'html':
	output_fileID.write( message )

################################################################################
message = '<h1><a name="jenkins">CellOrganizer CI Daily Report</a></h1>'
if tabulate_output_format == 'html':
	output_fileID.write( message )

message = '\nThis is an automated report from ' + username + '@' + computer + ' on ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z') + '.'
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

execfile( 'get_and_save_all_tickets.py' )
filename = 'list_of_cellorganizer_jenkins_jobs_' + datetime.datetime.now().strftime('%d-%b-%Y') +'.pkl'
list_of_jobs = pickle.load( file( filename, 'r'))

data = []
number_of_failing_jobs = 0
headers = ['NAME', 'STATUS', 'BUILDABLE', 'URL']
for job in list_of_jobs:
	try:
		if job['name'].startswith('cellorganizer') and job['name'].endswith('glnx64') and job['name'].find( 'issue' ) == -1 and job['name'].find( 'percellparam2') == -1 and job['name'].find('downsampling') == -1 and job['name'].find('gource') == -1 and job['name'].find('python') == -1:
			name = job['name']
			status = '<img src="http://developers.compbio.cs.cmu.edu:8080/static/a5ab88c2/images/32x32/"" + job['color'] + ".png"/>'
			url = '<a href='' + job['lastBuild']['url'] + ''>Last Build</a>'
			if job['buildable'] == True:
				buildable = 'True'
			else:
				buildable = 'False'
			datum = [name, status, buildable, url]
			if job['color'].find( 'red') and not job['color'].find( 'red-anime'):
				number_of_failing_jobs = number_of_failing_jobs + 1
			data.append( datum  )
	except:
		print 'Unable to retrieve information regarding this job.'

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( ' There are ' + str(len(data)) + ' jobs.')
	output_fileID.write( message )
else:
	print message

################################################################################
message = '<h1><a name="repository">CellOrganizer Repository Daily Report</a></h1>'
if tabulate_output_format == 'html':
	output_fileID.write( message )

message = '\nThis is an automated report from ' + username + '@' + computer + ' on ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z') + '.'
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

execfile( 'get_and_save_all_tickets.py' )
filename = 'list_of_cellorganizer_tickets_' + datetime.datetime.now().strftime('%d-%b-%Y') +'.pkl'
list_of_issues = pickle.load( file( filename, 'r'))

kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

message = 'List of Resolved Tickets by Date'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

resolved_issues = []
for issue in list_of_issues:
	try:
		if issue.has_key( 'status' ) and issue['status'] == 'resolved' or issue['status'] == 'closed' :
		  resolved_issues.append( issue['utc_last_updated'].split(' ')[0] )
	except:
		print ''

counter = collections.Counter([x for x in resolved_issues if x.startswith('2016')])
keys = counter.keys()
keys = [x.encode('UTF8') for x in keys]
values = counter.values()
[keys, values] = [list(x) for x in zip(*sorted(zip(keys, values), key=itemgetter(0)))]
message = tabulate( {'Date':keys, 'Frequency':values}, headers='keys', tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

message = 'List Open/New Issues per Author'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

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
		print ''

headers = ['AUTHOR']
headers.extend(  [x.upper() for x in kind] )
headers.extend( ['URL'] )

data = []
for author in list_of_issues_per_user:
	datum = [ author ]
	datum.extend( list_of_issues_per_user[ author ] )
	datum.extend( ['<a href='https://bitbucket.org/icaoberg/cellorganizer/issues?responsible=' + author + ''>Click Here</a>'])
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

kind = {'bug', 'task'}
status = {'new', 'open'}
message = 'Summary Open/New Issues per Version'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

message = 'https://bitbucket.org/icaoberg/cellorganizer/issues?kind=task&kind=bug&status=open&status=new'
if tabulate_output_format == 'html':
	output_fileID.write( 'To see all open tickets: <a href='' + message + ''>Click here</a>'  )
else:
	print 'To see all open tickets: ' + message

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
		print ''

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

message = 'Summary all Issues per Version'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

message = 'https://bitbucket.org/icaoberg/cellorganizer/issues?status=new&status=open'
if tabulate_output_format == 'html':
	output_fileID.write( 'To see all open tickets: <a href='' + message + ''>Click here</a>'  )
else:
	print 'To see all open tickets: ' + message

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
		print ''

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

message = 'Summary of all open issues'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

data = []
headers = ['ID', 'VER', 'TITLE', 'RESPONSIBLE', 'URL']
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

			url = '<a href='https://bitbucket.org/icaoberg/cellorganizer/issue/' + str(issue['local_id']) + ''>Click Here</a>'

			datum = [issue['local_id'], version, title, responsible, url]
			data.append( datum  )
	except:
		print ''

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

################################################################################
message = '<h1><a name="python">CellOrganizer for Python Daily Report</a></h1>'
if tabulate_output_format == 'html':
	output_fileID.write( message )

message = '\nThis is an automated report from ' + username + '@' + computer + ' on ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z') + '.'
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

execfile( 'get_and_save_all_tickets.py' )
filename = 'list_of_cellorganizer-python_tickets_' + datetime.datetime.now().strftime('%d-%b-%Y') +'.pkl'
list_of_issues = pickle.load( file( filename, 'r'))


kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

message = 'List of Resolved Tickets by Date'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

resolved_issues = []
for issue in list_of_issues:
	try:
		if issue.has_key( 'status' ) and issue['status'] == 'resolved' or issue['status'] == 'closed' :
		  resolved_issues.append( issue['utc_last_updated'].split(' ')[0] )
	except:
		print ''

counter = collections.Counter([x for x in resolved_issues if x.startswith('2016')])
if not counter:
	try:
		keys = counter.keys()
		keys = [x.encode('UTF8') for x in keys]
		values = counter.values()
		[keys, values] = [list(x) for x in zip(*sorted(zip(keys, values), key=itemgetter(0)))]
		message = tabulate( {'Date':keys, 'Frequency':values}, headers='keys', tablefmt=tabulate_output_format )
		if tabulate_output_format == 'html':
			output_fileID.write( message )
		else:
			print message

		message = 'List Open/New Issues per Author'
		if tabulate_output_format == 'html':
			output_fileID.write( '<h2>' + message + '</h2>' )
		else:
			print '\n' + banner( message.upper() )
	except:
		print 'Unable to count tickets. More than likely there are not tickets.'

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
		print ''

headers = ['AUTHOR']
headers.extend(  [x.upper() for x in kind] )
headers.extend( ['URL'] )

data = []
for author in list_of_issues_per_user:
	datum = [ author ]
	datum.extend( list_of_issues_per_user[ author ] )
	datum.extend( ['<a href='https://bitbucket.org/icaoberg/cellorganizer/issues?responsible=' + author + ''>Click Here</a>'])
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

kind = {'bug', 'task'}
status = {'new', 'open'}
message = 'Summary Open/New Issues per Version'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

message = 'https://bitbucket.org/icaoberg/cellorganizer/issues?kind=task&kind=bug&status=open&status=new'
if tabulate_output_format == 'html':
	output_fileID.write( 'To see all open tickets: <a href='' + message + ''>Click here</a>'  )
else:
	print 'To see all open tickets: ' + message

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
		print ''

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

message = 'Summary all Issues per Version'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

message = 'https://bitbucket.org/icaoberg/cellorganizer/issues?status=new&status=open'
if tabulate_output_format == 'html':
	output_fileID.write( 'To see all open tickets: <a href='' + message + ''>Click here</a>'  )
else:
	print 'To see all open tickets: ' + message

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
		print ''

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

message = 'Summary of all open issues'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

data = []
headers = ['ID', 'VER', 'TITLE', 'RESPONSIBLE', 'URL']
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

			url = '<a href='https://bitbucket.org/icaoberg/cellorganizer/issue/' + str(issue['local_id']) + ''>Click Here</a>'

			datum = [issue['local_id'], version, title, responsible, url]
			data.append( datum  )
	except:
		print ''

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

################################################################################
message = '<h1><a name="documentation">CellOrganizer Documentation Daily Report</a></h1>'
if tabulate_output_format == 'html':
	output_fileID.write( message )

message = '\nThis is an automated report from ' + username + '@' + computer + ' on ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z') + '.'
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

execfile( 'get_and_save_all_tickets.py' )
filename = 'list_of_cellorganizer-docs_tickets_' + datetime.datetime.now().strftime('%d-%b-%Y') +'.pkl'
list_of_issues = pickle.load( file( filename, 'r'))


kind = {'bug', 'task', 'proposal', 'enhancement'}
status = {'new', 'open'}

message = 'List of Resolved Tickets by Date'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

resolved_issues = []
for issue in list_of_issues:
	try:
		if issue.has_key( 'status' ) and issue['status'] == 'resolved' or issue['status'] == 'closed' :
		  resolved_issues.append( issue['utc_last_updated'].split(' ')[0] )
	except:
		print ''

counter = collections.Counter([x for x in resolved_issues if x.startswith('2016')])
if not counter:
	try:
		keys = counter.keys()
		keys = [x.encode('UTF8') for x in keys]
		values = counter.values()
		[keys, values] = [list(x) for x in zip(*sorted(zip(keys, values), key=itemgetter(0)))]
		message = tabulate( {'Date':keys, 'Frequency':values}, headers='keys', tablefmt=tabulate_output_format )
		if tabulate_output_format == 'html':
			output_fileID.write( message )
		else:
			print message

		message = 'List Open/New Issues per Author'
		if tabulate_output_format == 'html':
			output_fileID.write( '<h2>' + message + '</h2>' )
		else:
			print '\n' + banner( message.upper() )
	except:
		print 'Unable to count tickets. More than likely there are not tickets.'

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
		print ''

headers = ['AUTHOR']
headers.extend(  [x.upper() for x in kind] )
headers.extend( ['URL'] )

data = []
for author in list_of_issues_per_user:
	datum = [ author ]
	datum.extend( list_of_issues_per_user[ author ] )
	datum.extend( ['<a href='https://bitbucket.org/icaoberg/cellorganizer/issues?responsible=' + author + ''>Click Here</a>'])
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

kind = {'bug', 'task'}
status = {'new', 'open'}
message = 'Summary Open/New Issues per Version'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

message = 'https://bitbucket.org/icaoberg/cellorganizer/issues?kind=task&kind=bug&status=open&status=new'
if tabulate_output_format == 'html':
	output_fileID.write( 'To see all open tickets: <a href='' + message + ''>Click here</a>'  )
else:
	print 'To see all open tickets: ' + message

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
		print ''

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

message = 'Summary all Issues per Version'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

message = 'https://bitbucket.org/icaoberg/cellorganizer/issues?status=new&status=open'
if tabulate_output_format == 'html':
	output_fileID.write( 'To see all open tickets: <a href='' + message + ''>Click here</a>'  )
else:
	print 'To see all open tickets: ' + message

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
		print ''

headers = ['VERSION', 'NUMBER OF ISSUES']

data = []
for version in list_of_issues_per_version:
	datum = [ version ]
	datum.extend( [list_of_issues_per_version[ version ]] )
	data.append( datum )

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

message = 'Summary of all open issues'
if tabulate_output_format == 'html':
	output_fileID.write( '<h2>' + message + '</h2>' )
else:
	print '\n' + banner( message.upper() )

data = []
headers = ['ID', 'VER', 'TITLE', 'RESPONSIBLE', 'URL']
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

			url = '<a href='https://bitbucket.org/icaoberg/cellorganizer/issue/' + str(issue['local_id']) + ''>Click Here</a>'

			datum = [issue['local_id'], version, title, responsible, url]
			data.append( datum  )
	except:
		print ''

message = tabulate( data, headers, tablefmt=tabulate_output_format )
if tabulate_output_format == 'html':
	output_fileID.write( message )
else:
	print message

output_fileID.close()
