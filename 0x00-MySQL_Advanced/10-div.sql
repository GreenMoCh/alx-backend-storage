-- Creates a function SafeDiv

DROP FUNCTION IF EXISTS SafeDiv;
DELIMETER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    IF (b = 0)
    THEN
        RETURN (0);
    ELSE
        RETURN (a / b);
    END IF;
END
$$

DELIMETER ;
