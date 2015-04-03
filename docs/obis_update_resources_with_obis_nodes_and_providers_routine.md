# update_resources_with_obis_nodes_and_providers
database: [obis](../)  
schema: [obis](obis)  

    
    /*
     Created By: Mike Flavell
     Created On: 10 June 2013
     Purpose:    This is a function to update the obis.resources table with details of the obis node
                 and providers of a dataset. 
                 It will create a record in the obis node table if a node with the supplied name node does not exist.
                 it will update the ron_id of all resources with the specified provider_name.
                 It will update the provider_id of all resources with the specified provider_name.
     Parameters: 1 - Name of regional obis node (obis.ron), 
                 2 - Name of obis.provider to associate with node
     Outputs:    void (nothing)
    */
    
    
    
    	declare
    		_max_ron_id int; -- maximum value of ron id
    		_next_seq_number int; -- next value of ron id sequence number
    		_current_seq_number int; --current value of ron id sequence number
    		_ron_id int; -- id of the node we are interested in
    		_provider_id int; --id of the provider that we are interested in
    		_num_rows int; -- for diagnostics
    	begin
    
    	        if (TRIM(_ron_name) = '') then
    			raise warning 'No ron name was supplied';
    			return;
    		end if;
    
    		if (TRIM(_provider_name) = '') then
    			raise warning 'No provider name was supplied';
    			return;
    		end if;
    
    		/*
    
    		if (select exists (select 1 from obis.rons where ronname = _ron_name limit 1)) then
    			raise notice 'A node named "%" already exists in table obis.rons', _ron_name;
    		else
    		
    				-- we need to insert a new record into the obis.rons table
    
    				-- first check the sequence for the id is working ok
    				_max_ron_id := (select max(id) from obis.rons);
    				_next_seq_number := (select nextval(pg_get_serial_sequence('obis.rons', 'id')));
    				_current_seq_number := (select currval(pg_get_serial_sequence('obis.rons', 'id')));
    			
    				raise notice 'max ron id = %', to_char(_max_ron_id, '999');
    				raise notice 'current sequence number = %', to_char(_current_seq_number, '999');
    			       
    				if (_current_seq_number != _max_ron_id) then
    					raise notice 'updating obis.rons.id sequence';
    					perform setval(pg_get_serial_sequence('obis.rons', 'id'), _max_ron_id, true);
    				else
    					raise notice 'sequence does not need to be updated';
    				end if;
    				
    				raise notice 'inserting a new node with name "%" into obis.rons', _ron_name;
    				insert into obis.rons(ronname) values (_ron_name);
    				if found then
    					get diagnostics _num_rows = row_count;
    					raise notice 'inserted % rows(s)', _num_rows;
    				end if;
    			
    		end if;
    		*/
    		
    		---- get the id of the obis node
    		_ron_id := (select obis.create_node(_ron_name));
    		raise notice 'ron id = %', _ron_id;
    
                   -- check if we are ok to proceed
    	       if (_ron_id is null) then
    			raise warning 'Ron Id is null!';
    			return;
    	       end if;
    
    	       if (_ron_id = 0) then
    			raise warning 'Ron Id is 0!';
    			return;
    	       end if;
    		
    		-- get the id of the provider entry for this node
    		_provider_id := (select id from obis.providers where providername = _provider_name limit 1);
    		raise notice 'provider id = %', _provider_id;
    
    		-- check if we are ok to proceed
    		if (_provider_id is null) then
    			-- we can't do the update
    			raise warning 'A provider with name % could not be found!', _provider_name;
    		end if;
    
    		-- check if we are ok to proceed
    		if (_provider_id = 0) then
    			-- we can't do the update
    			raise warning 'Provider Id is 0!';
    		end if;
    
    		-- update the resources table with this node id
    		raise notice 'updating obis.resources setting ron_id = % (%) where provider_id = % (%)', _ron_id, _ron_name, _provider_id, _provider_name;
    		update obis.resources set ron_id = _ron_id where provider_id = _provider_id;
    
    		if found then
    			get diagnostics _num_rows = row_count;
    			raise notice 'updated % rows(s)', _num_rows;
    		end if;
    		
    		return;
    	end;
