-- SEARCH FUNCTION
CREATE OR REPLACE FUNCTION search_contacts(q TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, p.phone, c.email
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || q || '%'
       OR c.email ILIKE '%' || q || '%'
       OR p.phone LIKE '%' || q || '%';
END;
$$ LANGUAGE plpgsql;

-- UPSERT
CREATE OR REPLACE PROCEDURE upsert_user(
    p_first_name TEXT,
    p_last_name TEXT,
    p_phone TEXT
)
LANGUAGE plpgsql AS $$
DECLARE 
    cid INT;
BEGIN
    -- ищем контакт по имени и фамилии
    SELECT id INTO cid
    FROM contacts
    WHERE first_name = p_first_name
      AND last_name = p_last_name;

    IF cid IS NULL THEN
        -- если нет → создаём
        INSERT INTO contacts(first_name, last_name)
        VALUES (p_first_name, p_last_name)
        RETURNING id INTO cid;

        INSERT INTO phones(contact_id, phone, type)
        VALUES (cid, p_phone, 'mobile');

    ELSE
        -- если есть → обновляем телефон
        UPDATE phones
        SET phone = p_phone
        WHERE contact_id = cid;
    END IF;
END;
$$;

-- PAGINATION
CREATE OR REPLACE FUNCTION get_contacts(lim INT, off INT)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT c.first_name, p.phone
    FROM contacts c
    JOIN phones p ON c.id = p.contact_id
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;

-- ADD PHONE
-- CREATE OR REPLACE PROCEDURE add_phone(p_name TEXT, p_phone TEXT, p_type TEXT)
-- LANGUAGE plpgsql AS $$
-- DECLARE cid INT;
-- BEGIN
--     SELECT id INTO cid FROM contacts WHERE first_name = p_name;

--     IF cid IS NOT NULL THEN
--         INSERT INTO phones(contact_id, phone, type)
--         VALUES (cid, p_phone, p_type);
--     END IF;
-- END;
-- $$;
CREATE OR REPLACE PROCEDURE add_phone(
    p_name TEXT,
    p_phone TEXT,
    p_type TEXT
)
LANGUAGE plpgsql AS $$
DECLARE 
    cid INT;
BEGIN
    SELECT id INTO cid 
    FROM contacts 
    WHERE first_name = p_name;

    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;

-- MOVE TO GROUP
CREATE OR REPLACE PROCEDURE move_to_group(p_name TEXT, p_group TEXT)
LANGUAGE plpgsql AS $$
DECLARE gid INT;
DECLARE cid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group) RETURNING id INTO gid;
    END IF;

    SELECT id INTO cid FROM contacts WHERE first_name = p_name;
    UPDATE contacts SET group_id = gid WHERE id = cid;
END;
$$;

-- DELETE
CREATE OR REPLACE PROCEDURE delete_contact(p_query TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_query
       OR id IN (
           SELECT contact_id FROM phones WHERE phone = p_query
       );
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    invalid_data TEXT[] := '{}';
BEGIN
    -- цикл по массиву
    FOR i IN 1..array_length(names, 1) LOOP

        -- проверка телефона (только цифры и длина >= 6)
        IF phones[i] ~ '^[0-9]{6,}$' THEN

            -- вставка
            CALL upsert_user(names[i], phones[i]);

        ELSE
            -- сохраняем ошибочные данные
            invalid_data := array_append(
                invalid_data,
                names[i] || ':' || phones[i]
            );
        END IF;

    END LOOP;

    -- вывод ошибок
    RAISE NOTICE 'Invalid data: %', invalid_data;

END;
$$;