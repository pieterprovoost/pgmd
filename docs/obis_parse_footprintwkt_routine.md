# parse_footprintwkt
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE returnRecord obis.footprintwkt;
    DECLARE _temp TEXT;
    BEGIN
    
       returnRecord.slatitude := null;
       returnRecord.slongitude := null;
       returnRecord.elatitude := null;
       returnRecord.elongitude := null;
       
       if (_in is not null) then
    
    	_temp := UPPER(ltrim(rtrim(_in)));
    
    	if (_temp != '') then
    
    		returnRecord.slongitude := ST_XMIN(ST_ENVELOPE(ST_GEOMFROMTEXT(_temp, 4326)));
    		returnRecord.slatitude := ST_YMIN(ST_ENVELOPE(ST_GEOMFROMTEXT(_temp, 4326)));
    		returnRecord.elongitude:= ST_XMAX(ST_ENVELOPE(ST_GEOMFROMTEXT(_temp, 4326)));
    		returnRecord.elatitude := ST_YMAX(ST_ENVELOPE(ST_GEOMFROMTEXT(_temp, 4326)));
    
    	end if;
    
       end if;
    	
       RETURN returnRecord;
       
    END;
