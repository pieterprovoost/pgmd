# do_calcthemall
database: [obis](../)  
schema: [jcleary](jcleary)  

    
    
    /* Calculate indices
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		starttime timestamp with time zone;
    		endtime timestamp with time zone;
    		esx integer; -- constant specifying the number of specimens to use for es() calculation
    		
    	begin
    		set search_path to jcleary;
    		starttime:=clock_timestamp();
    		raise notice 'start function at %', starttime;
    	
    		perform do_calc('','','all','5d');
    		perform do_calc('','','all','1d');
    		
    		/*perform do_calc(' inner join iucn2014.redlist on redlist.valid_id=t0.valid_id',
    				' and redlist.red_list_status in (''EX'', ''EW'', ''CR'', ''EN'', ''VU'')',
    				'extovu','5d');
    		perform do_calc(' inner join iucn2014.redlist on redlist.valid_id=t0.valid_id',
    				' and redlist.red_list_status in (''EX'', ''EW'', ''CR'', ''EN'', ''VU'')',
    				'extovu','1d');
    		*/
    		
    		perform do_calc('',' and storedpath~''^x739909x738303x741923x762719x766931x766932x642142x''','mammals','5d');
    		perform do_calc('',' and storedpath~''^x739909x738303x741923x762719x766931x766932x642142x''','mammals','1d');
    		perform do_calc('',' and storedpath~''^x739909x738303x741923x762719x766931x766932x739377x''','birds','5d');
    		perform do_calc('',' and storedpath~''^x739909x738303x741923x762719x766931x766932x739377x''','birds','1d');
    		perform do_calc('',' and storedpath~''^x739909x738303x741923x762719x766931x766932x766933x517970x''','turtles','5d');
    		perform do_calc('',' and storedpath~''^x739909x738303x741923x762719x766931x766932x766933x517970x''','turtles','1d');
    		perform do_calc('',' and depth<100','shallow','5d');
    		perform do_calc('',' and depth<100','shallow','1d');
    		perform do_calc('',' and depth>=100','deep','5d');
    		perform do_calc('',' and depth>=100','deep','1d');
    	
    	--endtime:=clock_timestamp();
    	--retvar:='do_calctemall finished in '||endtime-starttime;
    	--return retvar;
    	return '';
    	end;
