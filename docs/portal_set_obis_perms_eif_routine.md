# set_obis_perms_eif
database: [obis](../)  
schema: [portal](portal)  

    
    
    /*
    FUNCTION:  set_obis_perms()
    
    Sets up various permissions for the OBIS Postgres database to allow connections
    via the OBIS portal server and potential administrative access.  Should be
    run after all the tables and schema are completed and the OBIS database has
    been completely built (basically the last step before distributing the database).
    
    The function assumes that three users/roles currently exist in the database and 
    should therefore be created first before running this script.  These users are
    "obisadmin", "obisportal", and "obisreader" and are essential for the proper
    operation of the OBIS mapping interface and web portal.
    
    The function sets permissions for the three OBIS user as follows:
    
    obisadmin  :  Owns all schemas and tables
    
    obisportal :  Owns the "portal" schema and tables
                  SELECT access to all schema and tables
               
    obisreader :  SELECT access to all schema and tables
    
    This function should be run as the "postgres" user.
    
    */
        
    DECLARE
        obj record;
        num integer;
        s varchar(255); -- return variable
            
    BEGIN
        raise notice 'Start of the function';
        num:=0;
    
        -- SCHEMA permissions
        FOR obj IN SELECT DISTINCT schemaname from pg_tables where schemaname in ('calc', 'col', 'geo', 'irmng', 'iucn', 'obis', 'portal', 'public', 'summaries', 'woa', 'worms' )
            LOOP
            EXECUTE 'ALTER SCHEMA ' || obj.schemaname || ' OWNER TO ' || 'obisadmin';
            EXECUTE 'GRANT ALL ON SCHEMA ' || obj.schemaname || ' TO ' || 'obisadmin';
            EXECUTE 'GRANT USAGE ON SCHEMA ' || obj.schemaname || ' TO ' || 'obisportal';
            EXECUTE 'GRANT USAGE ON SCHEMA ' || obj.schemaname || ' TO ' || 'obisreader';
            raise notice '%', obj.schemaname;
            END LOOP;
            
        -- TABLE permissions
            FOR obj IN SELECT schemaname, tablename from pg_tables where schemaname in ('calc', 'col', 'geo', 'irmng', 'iucn', 'obis', 'portal', 'public', 'summaries', 'woa', 'worms' )
        LOOP
            EXECUTE 'ALTER TABLE ' || obj.schemaname || '.' || obj.tablename || ' OWNER TO ' || 'obisadmin';
            EXECUTE 'GRANT ALL ON TABLE ' || obj.schemaname || '.' || obj.tablename || ' TO ' || 'obisadmin';
            EXECUTE 'GRANT SELECT ON TABLE ' || obj.schemaname || '.' || obj.tablename || ' TO ' || 'obisreader';
            EXECUTE 'GRANT SELECT ON TABLE ' || obj.schemaname || '.' || obj.tablename || ' TO ' || 'obisportal';
            raise notice '%', obj.schemaname || '.' || obj.tablename;
        END LOOP;
    
        
        -- 'portal' SCHEMA/TABLES
        EXECUTE 'GRANT ALL ON SCHEMA  portal TO obisportal';
        
        FOR obj IN SELECT schemaname, tablename from pg_tables where schemaname = 'portal'
        LOOP
            EXECUTE 'GRANT ALL ON TABLE ' || obj.schemaname || '.' || obj.tablename || ' TO ' || 'obisportal';
            raise notice '%', obj.schemaname || '.' || obj.tablename;
        END LOOP;
        
        EXECUTE 'GRANT ALL ON SEQUENCE portal.download_requests_oid_seq TO obisportal';
        EXECUTE 'GRANT ALL ON SEQUENCE portal.feedback_id_seq TO obisportal';
        
        
        RETURN num;
    end;
    
