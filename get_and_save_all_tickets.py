import cPickle as pickle
import os.path

execfile( 'bitbucket_connect.py' )
execfile( 'slack_connect.py' )

import os
print

import datetime

from tabulate import tabulate

from pyfiglet import Figlet
fig = Figlet(font='bubble')

################################################################################
slug = "cellorganizer"
bb = Bitbucket(username, password, slug)
[success, issues] = bb.issue.all()
number_of_issues = issues['count']

filename = "list_of_cellorganizer_tickets_" + datetime.datetime.now().strftime('%d-%b-%Y') +".pkl"

print "Attempting to retrieve tickets from the CellOrganizer repository"
if os.path.isfile( filename ):
	print "File " + filename + " found. Skipping retrieval."
else:
	tickets = []

	[anwser, repo] = bb.repository.get( slug )

	for issue_number in range( number_of_issues, 1, -1  ):
		[answer, issue] = bb.issue.get( issue_number )

		print "Appending issue: " + str(issue_number)
		tickets.append( issue )

	pickle.dump( tickets, open( filename, "wb" ) )

################################################################################
slug = 'pycellorganizer'
bb = Bitbucket(username, password, slug)
[success, issues] = bb.issue.all()
print success
number_of_issues = issues['count']

filename = "list_of_pycellorganizer_tickets_" + datetime.datetime.now().strftime('%d-%b-%Y') +".pkl"

print "Attempting to retrieve tickets from the CellOrganizer repository"
if os.path.isfile( filename ):
	print "File " + filename + " found. Skipping retrieval."
else:
	tickets = []

	[anwser, repo] = bb.repository.get( slug )

	for issue_number in range( number_of_issues, 1, -1  ):
		try:
			[answer, issue] = bb.issue.get( issue_number )

			print "Appending issue: " + str(issue_number)
			tickets.append( issue )
		except:
			print "Unable to get information about this ticket"

	pickle.dump( tickets, open( filename, "wb" ) )

################################################################################
slug = 'cellorganizer-docs'
bb = Bitbucket(username, password, slug)
[success, issues] = bb.issue.all()
number_of_issues = issues['count']

filename = "list_of_cellorganizer-docs_tickets_" + datetime.datetime.now().strftime('%d-%b-%Y') +".pkl"

print "Attempting to retrieve tickets from the CellOrganizer repository"
if os.path.isfile( filename ):
	print "File " + filename + " found. Skipping retrieval."
else:
	tickets = []

	[anwser, repo] = bb.repository.get( slug )

	for issue_number in range( number_of_issues, 1, -1  ):
		try:
			[answer, issue] = bb.issue.get( issue_number )

			print "Appending issue: " + str(issue_number)
			tickets.append( issue )
		except:
			print "Unable to get information about this ticket"

	pickle.dump( tickets, open( filename, "wb" ) )

################################################################################
slug = 'cellorganizer-python'
bb = Bitbucket(username, password, slug)
[success, issues] = bb.issue.all()
number_of_issues = issues['count']

filename = "list_of_cellorganizer-python_tickets_" + datetime.datetime.now().strftime('%d-%b-%Y') +".pkl"

print "Attempting to retrieve tickets from the CellOrganizer repository"
if os.path.isfile( filename ):
	print "File " + filename + " found. Skipping retrieval."
else:
	tickets = []

	[anwser, repo] = bb.repository.get( slug )

	for issue_number in range( number_of_issues, 1, -1  ):
		try:
			[answer, issue] = bb.issue.get( issue_number )

			print "Appending issue: " + str(issue_number)
			tickets.append( issue )
		except:
			print "Unable to get information about this ticket"

	pickle.dump( tickets, open( filename, "wb" ) )

################################################################################
execfile( 'jenkins_connect.py' )
filename = "list_of_cellorganizer_jenkins_jobs_" + datetime.datetime.now().strftime('%d-%b-%Y') +".pkl"

print "Attempting to retrieve jobs from the CellOrganizer CI"
if os.path.isfile( filename ):
	print "File " + filename + " found. Skipping retrieval."
else:
	list_of_jobs = server.get_jobs()
	jobs = []
	for job in list_of_jobs:
		print "Appending job: " + job['name']
		jobs.append(server.get_job_info(job['name']))

	pickle.dump( jobs, open( filename, "wb" ) )
