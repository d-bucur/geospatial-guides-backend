-- create table
CREATE TABLE spatial_test (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128),
  geom GEOMETRY(Point, 4326)
);

-- Add a spatial index
CREATE INDEX mytable_gix
  ON spatial_test
  USING GIST (geom);

-- Add points
INSERT INTO spatial_test (geom, name) VALUES (
  ST_GeomFromText('POINT(9.191948 45.464271)', 4326), 'Duomo'
);


INSERT INTO spatial_test (geom, name) VALUES (
  ST_GeomFromText('POINT(9.189508 45.467658)', 4326), 'Scala'
);


INSERT INTO spatial_test (geom, name) VALUES (
  ST_GeomFromText('POINT(9.189915 45.465962)', 4326), 'Galleria'
);


-- get distance from point in metres
select id, name, ST_DistanceSphere(ST_GeomFromText('POINT(9.189818 45.463292)', 4326), geom) as distance
from spatial_test


-- select points within radius (is most efficient?)
select *
from (
	select id, name, ST_DistanceSphere(ST_GeomFromText('POINT(9.189818 45.463292)', 4326), geom) as distance
	from spatial_test
) d
where distance < 300

-- more efficient, but unit is in degrees
SELECT *
FROM spatial_test
WHERE ST_DWithin(
	geom,
	ST_SetSRID(ST_MakePoint(9.189818, 45.463292), 4326),
	0.0025
)
