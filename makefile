# makefile for yelpDB

DBNAME = yelpDB
PRE_POPULATION = schema_pre.sql
POST_POPULATION = schema_post.sql
PY_POPULATION = populate_db.py

.PHONY: all create-db init-schema populate-data finalize-schema full-reset

all: full

create-db:
	createdb $(DBNAME)

init-schema:
	psql -d $(DBNAME) -f $(PRE_POPULATION)

populate-data:
	python3 $(PY_POPULATION)

finalize-schema:
	psql -d $(DBNAME) -f $(POST_POPULATION)

full: create-db init-schema populate-data finalize-schema

full-reset:
	dropdb --if-exists $(DBNAME)
	make full

