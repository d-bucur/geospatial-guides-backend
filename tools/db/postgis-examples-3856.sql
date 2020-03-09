-- create table
CREATE TABLE spatial_test_m (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128),
  geom GEOMETRY(Point, 3857)
);

-- Add a spatial index
CREATE INDEX mytable2_gix
  ON spatial_test_m
  USING GIST (geom);

-- Add points
INSERT INTO spatial_test_m (geom, name) VALUES (
	ST_Transform(ST_SetSRID(ST_MakePoint(9.191948, 45.464271), 4326), 3857), 'Duomo'
);
INSERT INTO spatial_test_m (geom, name) VALUES (
	ST_Transform(ST_SetSRID(ST_MakePoint(9.189508, 45.467658), 4326), 3857), 'Scala'
);
INSERT INTO spatial_test_m (geom, name) VALUES (
	ST_Transform(ST_SetSRID(ST_MakePoint(9.189915, 45.465962), 4326), 3857), 'Galleria'
);



-- get distance from point in metres
select id, name, ST_Distance(ST_Transform(ST_SetSRID(ST_MakePoint(9.189818, 45.463292), 4326), 3857), geom) as distance
from spatial_test_m


-- select points within radius (is most efficient?)
select *
from (
	select id, name, ST_DistanceSphere(ST_GeomFromText('POINT(9.189818 45.463292)', 3857), geom) as distance
	from spatial_test_m
) d
where distance < 300

-- more efficient, but unit is in degrees
SELECT *
FROM spatial_test_m
WHERE ST_DWithin(
	geom,
	ST_Transform(ST_SetSRID(ST_MakePoint(9.189818, 45.463292), 4326), 3857),
	700
)
