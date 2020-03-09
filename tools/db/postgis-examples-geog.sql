-- create table
CREATE TABLE spatial_test_g (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128),
  geog geography(POINT)
);

-- Add a spatial index
CREATE INDEX mytable_gig
  ON spatial_test_g
  USING GIST (geog);


INSERT INTO spatial_test_g (geog, name) VALUES (
  'SRID=4326;POINT(9.191948 45.464271)', 'Duomo'
);
INSERT INTO spatial_test_g (geog, name) VALUES (
  'POINT(9.189508 45.467658)', 'Scala'
);
INSERT INTO spatial_test_g (geog, name) VALUES (
  'POINT(9.189915 45.465962)', 'Galleria'
);

-- calculates distance from all places on db
select id, name, ST_Distance('POINT(9.189818 45.463292)', geog) as distance
from spatial_test_g


-- filters places within a certain distance from point
SELECT *
FROM spatial_test_g
WHERE ST_DWithin(
	geog,
	'POINT(9.189818 45.463292)',
	500
)