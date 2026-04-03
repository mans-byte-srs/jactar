create or replace procedure upsert_contact(p_name varchar, p_phone varchar)
language plpgsql as $$
begin
    if exists (select 1 from phonebook where name = p_name) then
        update phonebook set phone = p_phone where name = p_name;
    else
        insert into phonebook(name, phone) values (p_name, p_phone);
    end if;
end;
$$;

create or replace procedure bulk_insert_contacts(p_names varchar[], p_phones varchar[])
language plpgsql as $$
declare
    i int;
    bad_name varchar;
    bad_phone varchar;
    invalid_data text := '';
begin
    for i in 1 .. array_length(p_names, 1) loop
        bad_name := p_names[i];
        bad_phone := p_phones[i];

        if bad_phone ~ '^\+?[0-9]{7,15}$' then
            if exists (select 1 from phonebook where name = bad_name) then
                update phonebook set phone = bad_phone where name = bad_name;
            else
                insert into phonebook(name, phone) values (bad_name, bad_phone);
            end if;
        else
            invalid_data := invalid_data || bad_name || ' | ' || bad_phone || E'\n';
        end if;
    end loop;

    if invalid_data <> '' then
        raise notice 'invalid entries: %', invalid_data;
    end if;
end;
$$;

create or replace procedure delete_contact(p_name varchar default null, p_phone varchar default null)
language plpgsql as $$
begin
    if p_name is not null then
        delete from phonebook where name = p_name;
    elsif p_phone is not null then
        delete from phonebook where phone = p_phone;
    else
        raise exception 'provide at least name or phone';
    end if;
end;
$$;