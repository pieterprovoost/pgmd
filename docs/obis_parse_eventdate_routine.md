# parse_eventdate
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE returnRecord obis.eventdate;
    DECLARE temp_date TEXT;
    DECLARE date1 TEXT;
    DECLARE date2 TEXT;
    DECLARE startdate TEXT;
    DECLARE enddate TEXT;
    BEGIN
    
       returnRecord.startyearcollected  := null;
       returnRecord.startmonthcollected := null;
       returnRecord.startdaycollected := null;
       returnRecord.starttimecollected := null;
    
       returnRecord.endyearcollected  := null;
       returnRecord.endmonthcollected := null;
       returnRecord.enddaycollected := null;
       returnRecord.endtimecollected := null;
       
       if (date_in is not null) then
    
    	temp_date := ltrim(rtrim(date_in));
    
    	-- do we have more than 1 date?
    	if (strpos(temp_date, '/') > 0) then
    
              -- get both dates
              date1 := split_part(temp_date, '/', 1);
              date2 := split_part(temp_date, '/', 2);
    
              -- work out which is the earliest
              if ( obis.parse_iso_8601_date(date1) <= obis.parse_iso_8601_date(date2)) then
    		  startdate := date1;
    		  enddate := date2;
              else
    		  startdate := date2;
    		  enddate := date1;
              end if;
    
              --parse the 2 dates into the return fields;
              select 
              (obis.parse_iso_8601_date(startdate))._year, 
              (obis.parse_iso_8601_date(startdate))._month,
              (obis.parse_iso_8601_date(startdate))._day,
              ((obis.parse_iso_8601_date(startdate))._year || '-' ||  
              (obis.parse_iso_8601_date(startdate))._month || '-' || 
              (obis.parse_iso_8601_date(startdate))._day|| ' ' || 
              (obis.parse_iso_8601_date(startdate))._time :: time without time zone)::timestamp without time zone
              into returnRecord.startyearcollected, returnRecord.startmonthcollected, returnRecord.startdaycollected, returnRecord.starttimecollected;
    
              select
              (obis.parse_iso_8601_date(enddate))._year, 
              (obis.parse_iso_8601_date(enddate))._month,
              (obis.parse_iso_8601_date(enddate))._day,
              ((obis.parse_iso_8601_date(enddate))._year || '-' ||  
              (obis.parse_iso_8601_date(enddate))._month || '-' || 
              (obis.parse_iso_8601_date(enddate))._day|| ' ' || 
              (obis.parse_iso_8601_date(enddate))._time :: time without time zone)::timestamp without time zone
              into returnRecord.endyearcollected, returnRecord.endmonthcollected, returnRecord.enddaycollected, returnRecord.endtimecollected;
    	
    	-- we must only have 1 date.
    	else
    	        -- parse it into the start and end field;
    		select 
    		(obis.parse_iso_8601_date(temp_date))._year, 
    		(obis.parse_iso_8601_date(temp_date))._month,
    		(obis.parse_iso_8601_date(temp_date))._day,
    		((obis.parse_iso_8601_date(temp_date))._year || '-' ||  
    		(obis.parse_iso_8601_date(temp_date))._month || '-' || 
    		(obis.parse_iso_8601_date(temp_date))._day|| ' ' || 
    		(obis.parse_iso_8601_date(temp_date))._time :: time without time zone)::timestamp without time zone
    		into returnRecord.startyearcollected, returnRecord.startmonthcollected, returnRecord.startdaycollected, returnRecord.starttimecollected;
    		
    		select
    		(obis.parse_iso_8601_date(temp_date))._year, 
    		(obis.parse_iso_8601_date(temp_date))._month,
    		(obis.parse_iso_8601_date(temp_date))._day,
    		((obis.parse_iso_8601_date(temp_date))._year || '-' ||  
    		(obis.parse_iso_8601_date(temp_date))._month || '-' || 
    		(obis.parse_iso_8601_date(temp_date))._day|| ' ' || 
    		(obis.parse_iso_8601_date(temp_date))._time :: time without time zone)::timestamp without time zone
    		into returnRecord.endyearcollected, returnRecord.endmonthcollected, returnRecord.enddaycollected, returnRecord.endtimecollected;
    		
    	end if;
    
       end if;
    	
       RETURN returnRecord;
       
    END;
