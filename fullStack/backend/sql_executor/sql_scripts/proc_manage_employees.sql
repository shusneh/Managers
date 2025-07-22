DELIMITER $$

CREATE PROCEDURE manage_employees()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE emp_id INT;
    DECLARE emp_salary DECIMAL(10,2);
    DECLARE cur CURSOR FOR SELECT id, salary FROM employees;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO emp_id, emp_salary;
        IF done THEN
            LEAVE read_loop;
        END IF;

        IF emp_salary < 30000 THEN
            UPDATE employees SET salary = salary + 5000 WHERE id = emp_id;
        ELSEIF emp_salary < 50000 THEN
            UPDATE employees SET salary = salary + 3000 WHERE id = emp_id;
        ELSE
            UPDATE employees SET salary = salary + 1000 WHERE id = emp_id;
        END IF;

    END LOOP;

    CLOSE cur;
END $$

DELIMITER ;
