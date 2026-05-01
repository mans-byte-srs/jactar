create or replace function search_by_pattern(p text)
returns table(id int, name varchar, phone varchar) as $$
begin
    return query
        select c.id, c.name, c.phone
        from phonebook c
        where c.name ilike '%' || p || '%'
           or c.phone ilike '%' || p || '%';
end;
$$ language plpgsql;

create or replace function get_contacts_paginated(lim int, offs int)
returns table(id int, name varchar, phone varchar) as $$
begin
    return query
        select c.id, c.name, c.phone
        from phonebook c
        order by c.id
        limit lim offset offs;
end;
$$ language plpgsql;