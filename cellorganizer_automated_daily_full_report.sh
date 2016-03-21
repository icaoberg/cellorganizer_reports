#!/bin/bash

#activate virtual environment
source ./bin/activate

if [ $# -eq 0 ]; then
	EMAIL="icaoberg@gmail.com"
else
	EMAIL=$1
fi

OUTPUT_FILENAME="daily_report-"$(date +%Y-%m-%d)".html"
python cellorganicer_automated_daily_full_report.py

deactivate

#add borders to html tables. python tabulate does not add them
sed -i -- 's$<table>$<table border="1">$g' $OUTPUT_FILENAME

#send the results by email
cat $OUTPUT_FILENAME | mail -s "$(echo -e "CellOrganizer Daily Report\nContent-Type: text/html")" "$EMAIL"
