-- Write and execute a SQL query to list the school names, community names, and average attendance for communities with a hardship index of 98.

Select * FROM chicago_socioeconomic_data a LEFT JOIN chicago_public_schools b
ON a.community_area_number = b.community_area_number


Select * FROM chicago_public_schools a RIGHT JOIN chicago_socioeconomic_data b
ON a.community_area_number = b.community_area_number



-- Write and execute a SQL statement to create a view showing the columns listed in the following table, with new column names as shown in the second column.
CREATE OR REPLACE VIEW chopapi AS 
SELECT 
    NAME_OF_SCHOOL AS school_name,
    Safety_Icon AS safety_icon,
    Family_Involvement_Icon AS family_involvement_icon,
    Environment_Icon AS environment_icon,
    Instruction_Icon AS instruction_icon,
    Leaders_Icon AS leaders_icon,
    Teachers_Icon AS teachers_icon
FROM chicago_public_schools;
SELECT * FROM chopapi;

-- Write and execute a SQL query to list all crimes that took place at a school. Include case number, crime type, and community name.
SELECT a.case_number, a.primary_type, b.community_area_name
FROM chicago_crime_data a
JOIN chicago_public_schools b
ON a.location_description = b.name_of_school;
-- How many rows were returned upon execution of this query
Select count(*) FROM chicago_crime_data a
JOIN chicago_public_schools b
ON a.location_description = b.name_of_school;



-- Write the structure of a query to create or replace a stored procedure called UPDATE_LEADERS_SCORE that takes a in_School_ID parameter as an integer and a in_Leader_Score parameter as an integer.
 
CREATE OR REPLACE PROCEDURE UPDATE_LEADERS_SCORE (in_School_ID INT, in_Leader_Score INT)
-- Inside your stored procedure, write a SQL statement to update the Leaders_Score field in the CHICAGO_PUBLIC_SCHOOLS table for the school identified by in_School_ID to the value in the in_Leader_Score parameter.
BEGIN
    UPDATE chicago_public_schools
    SET Leaders_Score = in_Leader_Score
    WHERE school_id = in_School_ID;
-- Inside your stored procedure, write a SQL IF statement to update the Leaders_Icon field in the CHICAGO_PUBLIC_SCHOOLS table for the school identified by in_School_ID using the following information.
    IF in_Leader_Score > 80 THEN
        UPDATE chicago_public_schools
        SET Leaders_Icon = 'Very Strong'
        WHERE school_id = in_School_ID
END;

-- Write a query to call the stored procedure, passing a valid school ID and a leader score of 50, to check that the procedure works as expected.
CALL UPDATE_LEADERS_SCORE(610281, 50);
SELECT * FROM chicago_public_schools WHERE school_id = 610038;

-- Update your stored procedure definition. Add a generic ELSE clause to the IF statement that rolls back the current work if the score did not fit any of the preceding categories.
CREATE OR REPLACE PROCEDURE UPDATE_LEADERS_SCORE (in_School_ID INT, in_Leader_Score INT)
BEGIN
    UPDATE chicago_public_schools
    SET Leaders_Score = in_Leader_Score
    WHERE school_id = in_School_ID;
    IF in_Leader_Score > 80 THEN
        UPDATE chicago_public_schools
        SET Leaders_Icon = 'Very Strong'
        WHERE school_id = in_School_ID;
    ELSE
        ROLLBACK;
    END IF;
END;
-- Update your stored procedure definition again. Add a statement to commit the current unit of work at the end of the procedure.
CREATE OR REPLACE PROCEDURE UPDATE_LEADERS_SCORE (in_School_ID INT, in_Leader_Score INT)
BEGIN
    UPDATE chicago_public_schools
    SET Leaders_Score = in_Leader_Score
    WHERE school_id = in_School_ID;
    IF in_Leader_Score > 80 THEN
        UPDATE chicago_public_schools
        SET Leaders_Icon = 'Very Strong'
        WHERE school_id = in_School_ID;
    ELSE
        ROLLBACK;
    END IF;
    COMMIT;
END;
