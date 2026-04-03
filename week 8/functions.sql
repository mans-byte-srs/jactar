-- ФУНКЦИЯ 1: Поиск по паттерну (имя или телефон)
CREATE OR REPLACE FUNCTION search_by_pattern(p TEXT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.surname, c.phone
        FROM phonebook c
        WHERE c.name    ILIKE '%' || p || '%'
           OR c.surname ILIKE '%' || p || '%'
           OR c.phone   ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

-- Вызов:  SELECT * FROM search_by_pattern('Ali');
-- ФУНКЦИЯ 2: Пагинация (страницы)
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE(id INT, name VARCHAR, surname VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
        SELECT c.id, c.name, c.surname, c.phone
        FROM phonebook c
        ORDER BY c.id
        LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;

-- Вызов:  SELECT * FROM get_contacts_paginated(5, 0);  -- первые 5
--         SELECT * FROM get_contacts_paginated(5, 5);  -- следующие 5