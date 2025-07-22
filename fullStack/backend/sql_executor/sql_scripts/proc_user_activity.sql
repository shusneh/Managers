DELIMITER $$

CREATE PROCEDURE track_user_activity()
BEGIN
    DECLARE last_user_id INT DEFAULT 0;
    DECLARE max_id INT;

    SELECT MAX(user_id) INTO max_id FROM user_logs;

    WHILE last_user_id < max_id DO
        SET last_user_id = last_user_id + 1;

        IF EXISTS (SELECT 1 FROM user_logs WHERE user_id = last_user_id AND action = 'login') THEN
            INSERT INTO user_summary(user_id, status) VALUES (last_user_id, 'Active');
        ELSE
            INSERT INTO user_summary(user_id, status) VALUES (last_user_id, 'Inactive');
        END IF;
    END WHILE;
END $$

DELIMITER ;
