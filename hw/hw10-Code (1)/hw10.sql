.read hw10_data.sql

-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name, size FROM dogs, sizes where min < height and height <= max;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT ch.name from dogs as ch, dogs as pa,parents as a where ch.name = a.child and a.parent = pa.name order by pa.height desc ;

CREATE TABLE syblings AS
  SELECT a.child as a, b.child as b, c.size from parents as a, parents as b, size_of_dogs as c, size_of_dogs as d where a.parent = b.parent and a.child < b.child and c.name = a.child and d.name = b.child and c.size = d.size; 
-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || a ||" plus "||b||" have the same size: "||size from syblings;



-- The almighty midterm score of the SICP'25 students
CREATE TABLE midterm_almighty AS
  SELECT max(p1_wwpd)+max(p2_env)+max(p3_lists)+max(p4_functions)+max(p5_abstraction)+max(p6_tests)+max(p7_generators)+max(p8_bonus) as total from midterm;

CREATE TABLE standard AS
  SELECT '90.0' AS level, 90 AS min, 103 AS max UNION
  SELECT '80.0'       , 80       , 90        UNION
  SELECT '70.0'     , 70       , 80      UNION
  SELECT '60.0'       , 60       , 70        UNION
  SELECT '50.0'       , 50       , 60        UNION
  SELECT '40.0'       , 40       , 50        UNION
  SELECT '30.0'       , 30       , 40        UNION
  SELECT '20.0'   , 20       , 30;  
CREATE TABLE helper AS 
  SELECT student_id, level from midterm, standard where total >= min and total < max;
-- The total score distribution of SICP'25 midterm exam
CREATE TABLE midterm_distribution AS
  SELECT level,count(*) from helper group by (level) order by level desc;
