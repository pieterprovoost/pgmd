# mf_clean_sauthor
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE
       old_sauthor varchar(200);
    BEGIN
    
       cleaned_sauthor := trim(lower(sauthor)); -- assign in case there are no matches
       matched := false; -- set flag
    
       if sauthor = '' then
    	return;
       end if;
    
      -- NOTE THAT THE ORDER OF THE REPLACEMENTS BELOW IS IMPORTANT
    
       old_sauthor := cleaned_sauthor; -- store the name before cleaning
    
       -- REPLACEMENTS
       cleaned_sauthor:= (select trim(replace(cleaned_sauthor, '"', ' '))); -- replace double quote with a space
       cleaned_sauthor:= (select trim(replace(cleaned_sauthor, ',', ' '))); -- replace comma with a space
       cleaned_sauthor:= (select trim(replace(cleaned_sauthor, '.', ' '))); -- replace comma with a space
       
       cleaned_sauthor:= (select trim(replace(cleaned_sauthor, '(', ' '))); -- replace comma with a space
       cleaned_sauthor:= (select trim(replace(cleaned_sauthor, ')', ' '))); -- replace comma with a space
       
       --cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '^[(]?', ''))); -- remove bracket at the start of a line
       --cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '[)]?$', ''))); -- remove bracket at the end of a line
       cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '[0-9]{4}$', ''))); -- remove first occurrence of a 4 digit sequence (i.e. date)
       cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '[ ]+', ' '))); -- replace multiple spaces with a single space
       cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '[&]+$', ''))); -- remove &'s at the end of a name
       cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '^[+]+', ''))); -- remove +'s at the start of a name
    
       cleaned_sauthor:= (select trim(replace(cleaned_sauthor, 'mller', 'müller')));
       --cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '^mller ', 'müller ')));
       --cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, ' mller$', ' müller')));
    
       cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, ' [a-z] ', ' ')));
       cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, '^[a-z] ', ' ')));
       cleaned_sauthor:= (select trim(regexp_replace(cleaned_sauthor, ' [a-z]$', ' ')));
       
       if not (cleaned_sauthor = old_sauthor) then
    	matched := true;
       end if;
       
       return;
       
    END;
