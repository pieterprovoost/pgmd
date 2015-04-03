# process_tnames_audit
database: [obis](../)  
schema: [obis](obis)  

    
        begin
            --
            -- Create a row in tnamearchive to reflect the operation performed on tnames,
            -- make use of the special variable TG_OP to work out the operation.
            --
            if (tg_op = 'DELETE') then
                insert into obis.tnamearchive(
                operation, who, whe, tname_id, tname, tauthor, valid_id, display, 
                displayremark, rank_id, parent_id, storedpath, worms_id, col_id, 
                irmng_id, itis_id, ncbi_id, notes)
                select 'D', user, now(), old.id, old.tname, old.tauthor, old.valid_id, old.display, 
                old.displayremark, old.rank_id, old.parent_id, old.storedpath, old.worms_id, old.col_id, 
                old.irmng_id, old.itis_id, null, null;
                return old;
            elseif (tg_op = 'UPDATE') then
                insert into obis.tnamearchive(
                operation, who, whe, tname_id, tname, tauthor, valid_id, display, 
                displayremark, rank_id, parent_id, storedpath, worms_id, col_id, 
                irmng_id, itis_id, ncbi_id, notes) 
                select 'U', user, now(), old.id, old.tname, old.tauthor, old.valid_id, old.display, 
                old.displayremark, old.rank_id, old.parent_id, old.storedpath, old.worms_id, old.col_id, 
                old.irmng_id, old.itis_id, null, null;
                return new;
            elseif (tg_op = 'INSERT') then
                insert into obis.tnamearchive(
                operation, who, whe, tname_id, tname, tauthor, valid_id, display, 
                displayremark, rank_id, parent_id, storedpath, worms_id, col_id, 
                irmng_id, itis_id, ncbi_id, notes) 
                select 'I', user, now(), new.id, new.tname, new.tauthor, new.valid_id, new.display, 
                new.displayremark, new.rank_id, new.parent_id, new.storedpath, new.worms_id, new.col_id, 
                new.irmng_id, new.itis_id, null, null;
                return new;
            end if;
            return null; -- result is ignored since this is an AFTER trigger
        end;
