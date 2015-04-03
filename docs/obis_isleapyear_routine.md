# isleapyear
database: [obis](../)  
schema: [obis](obis)  

    
    BEGIN
    	-- A year will be a leap year if it is divisible by 4 but not by 100
    	IF ((Year % 4 = 0) AND (Year % 100 <> 0)) THEN
    		RETURN true;
    	-- If a year is divisible by 4 and by 100,
    	ELSE
    	  --it is not a leap year unless it is also divisible by 400.
    	  IF (Year % 400 = 0) THEN
    		RETURN true;
    	  END IF;
    	  
    	END IF;
    	
    	RETURN false;
    END	
