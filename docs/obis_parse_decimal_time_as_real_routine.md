# parse_decimal_time_as_real
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE temp_time TEXT;
    DECLARE _hours TEXT;
    DECLARE _time_in text;
    DECLARE _remainder DOUBLE PRECISION;
    DECLARE _minutes INT;
    DECLARE _seconds INT;
    DECLARE time2 TEXT;
    DECLARE starttime TEXT;
    DECLARE endtime TEXT;
    DECLARE r time without time zone;
    DECLARE twtz_time2 time without time zone;
    DECLARE temp_t_time character varying(100);
    BEGIN
    	r := null;
    	_time_in := trim(regexp_replace(time_in, E' \+00:00$', ''));
    	_time_in := trim(regexp_replace(time_in, E' 00:00$', ''));
    	RETURN _time_in::real;
    	
    exception
        when invalid_text_representation then
            return null;
    END;
