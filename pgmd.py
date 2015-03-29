import psycopg2
import os
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

# scripts

script_schemas = open("schemas.sql", "r").read()
script_tables = open("tables.sql", "r").read()
script_views = open("views.sql", "r").read()
script_routines = open("routines.sql", "r").read()

# schemas

cur = conn.cursor()
cur.execute(script_schemas)
schemas = cur.fetchall()

# tables

cur = conn.cursor()
cur.execute(script_tables)
tables = cur.fetchall()

# views

cur = conn.cursor()
cur.execute(script_views)
views = cur.fetchall()

# routines

cur = conn.cursor()
cur.execute(script_routines)
routines = cur.fetchall()

# create output directory

if not os.path.exists('output'):
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
		f.write('[' + tablename + '](' + schema + '_' + tablename + ')  \n')

	# views

	f.write('### views\n')
	schemaviews = [view for view in views if view[0] == schema]
	for view in schemaviews:
		viewname = view[1]
		f.write('[' + viewname + '](' + schema + '_' + viewname + ')  \n')

	# routines

	f.write('### routines\n')
	schemaroutines = [routine for routine in routines if routine[0] == schema]
	for routine in schemaroutines:
		routinename = routine[1]
		routinelang = routine[2]
		f.write('[' + routinename + '](' + schema + '_' + routinename + ') ' + routinelang + '  \n')

# close file

f.close()
