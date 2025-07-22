DELIMITER $$

CREATE PROCEDURE generate_employee_report()
BEGIN
    DECLARE dept_id INT DEFAULT 1;

    WHILE dept_id <= 3 DO
        INSERT INTO employee_reports (department_id, total_employees, avg_salary)
        SELECT 
            dept_id,
            COUNT(*),
            AVG(salary)
        FROM employees
        WHERE department_id = dept_id;

        SET dept_id = dept_id + 1;
    END WHILE;
END $$

DELIMITER ;
