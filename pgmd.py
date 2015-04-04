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

# create link

def link(name, url):
	return '[' + name + '](' + url + ')'

# excludes

excludes = tuple(item.strip() for item in parser.get('schema', 'exclude').split(','))

# scripts

script_schemas = open("queries/schemas.sql", "r").read()
script_tables = open("queries/tables.sql", "r").read()
script_views = open("queries/views.sql", "r").read()
script_routines = open("queries/routines.sql", "r").read()
script_columns = open("queries/columns.sql", "r").read()
script_constraints = open("queries/constraints.sql", "r").read()
script_triggers = open("queries/triggers.sql", "r").read()

# database

dbname = parser.get('database', 'dbname')

# schemas

cur = conn.cursor()
cur.execute(script_schemas, (excludes,))
schemas = cur.fetchall()

# tables

cur.execute(script_tables, (excludes,))
tables = cur.fetchall()

# views

cur.execute(script_views, (excludes,))
views = cur.fetchall()

# routines

cur.execute(script_routines, (excludes,))
routines = cur.fetchall()

# columns

cur.execute(script_columns, (excludes,))
columns = cur.fetchall()

# constraints

cur.execute(script_constraints, (excludes,))
constraints = cur.fetchall()

# triggers

cur.execute(script_triggers, (excludes,))
triggers = cur.fetchall()

# output directory

if os.path.exists('docs'):
	for the_file in os.listdir('docs'):
	    file_path = os.path.join('docs', the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception, e:
	        print e
else:
	os.makedirs('docs')

# create index file

f = open('docs/' + dbname + '.md', 'w')
f.write('# ' + dbname + '\n')
f.write('##  schemas\n')

# schema list

for schema in [s[0] for s in schemas]:
	f.write(link(schema, dbname + '_' + schema) + '  \n')

# schemas

for schema in [s[0] for s in schemas]:

	# schema file

	fs = open('docs/' + dbname + '_' + schema + '.md', 'w')
	fs.write('# ' + schema + '\n')
	fs.write('database: ' + link(dbname, dbname) + '  \n')

	# tables

	fs.write('## tables\n')
	schematables = [table for table in tables if table[0] == schema]
	for table in schematables:
		tablename = table[1]
		tableconstraints = [constraint for constraint in constraints if constraint[0] == schema and constraint[1] == tablename]

		fs.write(link(tablename, dbname + '_' + schema + '_' + tablename) + '  \n')

		# table file

		ft = open('docs/' + dbname + '_' + schema + '_' + tablename + '.md', 'w')

		ft.write('# ' + tablename + '\n')
		ft.write('database: ' + link(dbname, dbname) + '  \n')
		ft.write('schema: ' + link(schema, dbname + '_' + schema) + '  \n\n')

		# columns

		ft.write('|Column|Type|Constraint|\n')
		ft.write('|:---|:---|:---|\n')
		tablecolumns = [column for column in columns if column[0] == schema and column[1] == tablename]
		for column in tablecolumns:
			columnname = column[2]
			columntype = column[5]
			ft.write('|' + columnname)
			ft.write('|' + columntype)

			# constraints

			ft.write('|')
			columnconstraints = [constraint for constraint in tableconstraints if columnname in constraint[8]]	
			for constraint in columnconstraints:
				if constraint[5] == 'f':
					ftablename = constraint[3]
					fschemaname = constraint[2]
					ft.write(link(constraint[4], dbname + '_' + fschemaname + '_' + ftablename) + ' ')
				elif constraint[5] == 'p':
					ft.write(constraint[4] + ' ')
				elif constraint[5] == 'u':
					ft.write(constraint[4] + ' ')
				elif constraint[5] == 'c':
					ft.write(constraint[4] + ' ')
			ft.write('|\n')					
		ft.write('\n')					

		# triggers

		ft.write('## triggers\n\n')
		ft.write('|Name|Procedure|Constraint|Type|Event|Action|\n')
		ft.write('|:---|:---|:---|:---|:---|:---|\n')
		tabletriggers = [trigger for trigger in triggers if column[1] == schema and column[2] == tablename]
		for trigger in tabletriggers:
			triggername = column[0]
			proc = column[4]
			conschema = column[5]
			conname = column[6]
			ttype = column[7]
			tevent = column[8]
			taction = column[9]
			ft.write('|' + triggername)
			ft.write('|' + proc)
			ft.write('|' + conname)
			ft.write('|' + ttype)
			ft.write('|' + tevent)
			ft.write('|' + taction)
			ft.write('|\n')
		ft.write('\n')					
		ft.close()

	# views

	fs.write('## views\n')
	schemaviews = [view for view in views if view[0] == schema]
	for view in schemaviews:
		viewname = view[1]
		viewdef = view[2]
		fs.write(link(viewname, dbname + '_' + schema + '_' + viewname) + '  \n')

		# view file

		fr = open('docs/' + dbname + '_' + schema + '_' + viewname + '.md', 'w')
		fr.write('# ' + viewname + '\n')
		fr.write('database: ' + link(dbname, dbname) + '  \n')
		fr.write('schema: ' + link(schema, dbname + '_' + schema) + '  \n\n')

		fr.write(formatc(viewdef))
		fr.close()

	# routines

	fs.write('## routines\n')
	schemaroutines = [routine for routine in routines if routine[0] == schema]
	for routine in schemaroutines:
		routinename = routine[1]
		routinelang = routine[5]
		routinesrc = routine[2]
		if routinename is not None:
			fs.write(link(routinename, dbname + '_' + schema + '_' + routinename) + '  \n')

			# routine file

			fr = open('docs/' + dbname + '_' + schema + '_' + routinename + '.md', 'w')
			fr.write('# ' + routinename + '\n')
			fr.write('database: ' + link(dbname, dbname) + '  \n')
			fr.write('schema: ' + link(schema, dbname + '_' + schema) + '  \n\n')

			fr.write(formatc(routinesrc))
			fr.close()

	# close schema file

	fs.close()

# close index file

f.close()