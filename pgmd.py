import psycopg2
import os
import shutil
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('pgmd.ini')

try:
	conn = psycopg2.connect(
		dbname=parser.get('database', 'dbname'),
		user=parser.get('database', 'user'),
		host=parser.get('database', 'host'),
		password=parser.get('database', 'password'))
except:
	print "Cannot connect to the database"

# reformat code

def formatc(source):
	return '    ' + '    '.join(source.splitlines(True))

# excluses

excludes = tuple(item.strip() for item in parser.get('schema', 'exclude').split(','))

# scripts

script_schemas = open("schemas.sql", "r").read()
script_tables = open("tables.sql", "r").read()
script_views = open("views.sql", "r").read()
script_routines = open("routines.sql", "r").read()
script_columns = open("columns.sql", "r").read()

# schemas

cur = conn.cursor()
cur.execute(script_schemas, (excludes,))
schemas = cur.fetchall()

# tables

cur = conn.cursor()
cur.execute(script_tables, (excludes,))
tables = cur.fetchall()

# views

cur = conn.cursor()
cur.execute(script_views, (excludes,))
views = cur.fetchall()

# routines

cur = conn.cursor()
cur.execute(script_routines, (excludes,))
routines = cur.fetchall()

# columns

cur = conn.cursor()
cur.execute(script_columns, (excludes,))
columns = cur.fetchall()

# output directory

if os.path.exists('output'):
	for the_file in os.listdir('output'):
	    file_path = os.path.join('output', the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception, e:
	        print e
else:
	os.makedirs('output')

# create index file

f = open('output/index.md', 'w')
f.write('# ' + parser.get('database', 'dbname') + '\n')
f.write('##  schemas\n')

# schema list

for schema in [s[0] for s in schemas]:
	f.write('[' + schema + '](#' + schema + ')  \n')

# schemas

for schema in [s[0] for s in schemas]:
	f.write('<a name="' + schema + '"></a>\n')
	f.write('## ' + schema + '\n')

	# tables

	f.write('### tables\n')
	schematables = [table for table in tables if table[0] == schema]
	for table in schematables:
		tablename = table[1]
		f.write('[' + tablename + '](' + schema + '_' + tablename + '_table)  \n')

		ft = open('output/' + schema + '_' + tablename + '_table.md', 'w')
		ft.write('# ' + tablename + '\n')
		ft.write('|Column|Type|\n')
		ft.write('|:---|:---|\n')
		tablecolumns = [column for column in columns if column[1] == tablename]
		for column in tablecolumns:
			columnname = column[2]
			columntype = column[5]
			ft.write('|' + columnname + '|' + columntype + '|\n')
		ft.close()

	# views

	f.write('### views\n')
	schemaviews = [view for view in views if view[0] == schema]
	for view in schemaviews:
		viewname = view[1]
		viewdef = view[2]
		f.write('[' + viewname + '](' + schema + '_' + viewname + '_view)  \n')

		fr = open('output/' + schema + '_' + viewname + '_view.md', 'w')
		fr.write('# ' + viewname + '\n')
		fr.write(formatc(viewdef))
		fr.close()

	# routines

	f.write('### routines\n')
	schemaroutines = [routine for routine in routines if routine[0] == schema]
	for routine in schemaroutines:
		routinename = routine[1]
		routinelang = routine[5]
		routinesrc = routine[2]
		if routinename is not None:
			f.write('[' + routinename + '](' + schema + '_' + routinename + '_routine) ' + routinelang + '  \n')

			fr = open('output/' + schema + '_' + routinename + '_routine.md', 'w')
			fr.write('# ' + routinename + '\n')
			fr.write(formatc(routinesrc))
			fr.close()

# close index file

f.close()
