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
  SELECT max(p1_wwpd)+max(p2_env)+max(p3_lists)+max(p4_functions)+max(p5_abstraction)+max(p6_tests)+max(p7_generators)+max(p8_bonus) as total from midterm


-- The total score distribution of SICP'25 midterm exam
CREATE TABLE midterm_distribution AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";
