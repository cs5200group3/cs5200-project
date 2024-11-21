DELIMITER $$

CREATE TRIGGER validate_phone_length_before_insert
BEFORE INSERT ON Account
FOR EACH ROW
BEGIN

    IF CHAR_LENGTH(NEW.phone) > 14 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Phone number cannot exceed 14 characters.';
    END IF;
END$$

DELIMITER ;
