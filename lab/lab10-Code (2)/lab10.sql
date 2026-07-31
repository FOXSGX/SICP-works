.read lab10_data.sql


CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = 'blue' AND pet = 'dog';

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students WHERE color = 'blue' AND pet = 'dog';


CREATE TABLE smallest_int_having AS
  SELECT time,MIN(smallest) FROM students GROUP BY smallest HAVING COUNT(*) = 1;


CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color FROM students AS a, students AS b WHERE a.pet = b.pet AND a.song = b.song AND a.time < b.time ;


CREATE TABLE sevens AS
  SELECT seven FROM students AS s, numbers AS n WHERE number = 7 AND n."7" = 'True' AND s.time = n.time;


CREATE TABLE avg_difference AS
  SELECT round(avg(abs(number-smallest))) FROM students;


CREATE TABLE correlation AS
  SELECT "REPLACE THIS LINE WITH YOUR SOLUTION";
