-- Auxiliary queries to get statistics from the database

-- Show number of connections by means of transport
select means_transport, count(means_transport) from Connection group by means_transport
                                                               order by count(means_transport), means_transport;

-- Show number of connections by way
select way, count(way) from Connection group by way order by count(way), way;

-- Sort connections by length
select location_a, location_b, way, means_transport, distance from Connection order by distance, means_transport, location_a, location_b;
select location_a, location_b, way, means_transport, distance from Connection where means_transport = 'Car' order by distance, means_transport, location_a, location_b;
select location_a, location_b, way, means_transport, distance from Connection where means_transport = 'Boat' order by distance, means_transport, location_a, location_b;
select location_a, location_b, way, means_transport, distance from Connection where means_transport = 'Train' order by distance, means_transport, location_a, location_b;
select location_a, location_b, way, means_transport, distance from Connection where means_transport = 'High-Speed Train' order by distance, means_transport, location_a, location_b;
select location_a, location_b, way, means_transport, distance from Connection where means_transport = 'Plane' order by distance, means_transport, location_a, location_b;

-- Show number of destinations by appearance
select destination, count(destination) from Destination group by destination order by count(destination), destination;
select destination, count(destination) from Destination where destination = 'Lisboa' group by destination;
select destination, count(destination) from Destination where destination like '%Lisboa%' group by destination order by count(destination), destination;
select count(destination) from Destination where destination like '%Lisboa%';

-- Show number of Portuguese locations by parish, municipality, district, intermunicipal entity and region, respectively
select parish, concelho, count(parish) from LocationPortugal group by parish, concelho
                                                             order by count(parish), parish, concelho;
select concelho, count(concelho) from LocationPortugal group by concelho order by count(concelho), concelho;
select district, count(district) from LocationPortugal, Concelho where LocationPortugal.concelho = Concelho.concelho
                                                                 group by district order by count(district);
select intermunicipal_entity, count(intermunicipal_entity) from LocationPortugal, Concelho
                                                               where LocationPortugal.concelho = Concelho.concelho
                                                               group by intermunicipal_entity
                                                               order by count(intermunicipal_entity), intermunicipal_entity;
select region, count(region) from LocationPortugal, Concelho where LocationPortugal.concelho = Concelho.concelho
                                                             group by region order by count(region), region;

-- Show number of Spanish locations by district, municipality, comarca, province and autonomous community, respectively

select district, municipio, count(district) from LocationSpain where district is not null
                                                               group by district, municipio
                                                               order by count(district), municipio, district;

select municipio, count(municipio) from LocationSpain group by municipio order by count(municipio), municipio;

select comarca, Municipio.province, count(comarca)
from Comarca, Municipio, LocationSpain
where Comarca.municipio = Municipio.municipio and LocationSpain.municipio = Municipio.municipio
group by comarca, Municipio.province
order by count(comarca), Municipio.province, comarca;

select province, count(province) from LocationSpain group by province order by count(province), province;

select autonomous_community, count(autonomous_community)
from LocationSpain, Municipio, Province
where LocationSpain.municipio = Municipio.municipio and Municipio.province = Province.province
group by autonomous_community
order by count(autonomous_community), autonomous_community;

-- Shows all Spanish districts and respective municipalities with locations in the map
select distinct municipio, district from LocationSpain where district is not null order by municipio, district;

-- Show number of locations by protected area
select protected_area, count(protected_area) from Location group by protected_area order by count(protected_area), protected_area;

-- Show number of Portuguese, Spanish and Gibraltar locations, respectively
select count(name) as "Locations in Portugal" from LocationPortugal;
select count(name) as "Locations in Spain" from LocationSpain;
select count(name) as "Locations in Gibraltar" from LocationGibraltar;

-- Order locations by altitude, latitude and longitude, respectively
select name, altitude from Location order by altitude, name;
select name, latitude from Location order by latitude, name;
select name, longitude from Location order by longitude, name;

-- Show locations with max and min latitude, longitude and altitude
select name, latitude, longitude from Location where latitude = (select max(latitude) from Location);
select name, latitude, longitude from Location where latitude = (select min(latitude) from Location);
select name, latitude, longitude from Location where longitude = (select min(longitude) from Location);
select name, latitude, longitude from Location where longitude = (select max(longitude) from Location);
select name, latitude, longitude, altitude from Location where altitude = (select max(altitude) from Location);

-- Show connections featuring destinations, by number of destinations. Directions are shown separately
-- Ex: (Lisbon -> Oporto and Oporto -> Lisbon appear separately)
select Destination.location_a, Destination.location_b, Destination.starting_point, Destination.means_transport, Connection.way, count(*)
from Destination, Connection
where Destination.location_a = Connection.location_a and Destination.location_b = Connection.location_b and Destination.means_transport = Connection.means_transport
group by Destination.location_a, Destination.location_b, Destination.starting_point, Destination.means_transport, Connection.way
order by count(*), Destination.location_a, Destination.location_b, Destination.starting_point, Destination.means_transport, Connection.way;

-- Show ways by total length of connections associated to each way
select way, sum(distance), count(distance) from Connection group by way order by sum(distance), way;

-- Shows average connection length for connections
select way, round(sum(distance) / count(distance), 2) as "Distance per connection", sum(distance), count(distance) from Connection group by way order by sum(distance) / count(distance) desc, way;

-- Show total length and number of connections associated to A-7 (Autovía del Mediterráneo) and AP-7 (Autopista del Mediterráneo)
select sum(distance) as "Total distance of A-7 and AP-7", count(distance) as "Number of connections of A-7 and AP-7"
from Connection
where (way like '%A-7%' or way like '%AP-7%');

-- Show total length and number of connections associated to the Portuguese North Line
select sum(distance) as "Total distance of the North Line connections", count(distance) as "Number of connections of the North Line"
from Connection
where way like 'Linha do Norte - %';

-- Show ways by total number of destinations associated to connections of each way
-- Destination names may appear repeatedly (ex: Lisbon and Oporto are destinations associated to virtually all connections of A1)
select way, count(destination)
from Destination, Connection
where Destination.location_a = Connection.location_a and Destination.location_b = Connection.location_b and Destination.means_transport = Connection.means_transport
group by way
order by count(destination), way;

-- Show connection info associated with coordinates of locations
select location1.latitude, location1.longitude, location2.latitude, location2.longitude, Connection.way, Connection.means_transport
from Location as location1, Location as location2, Connection
where location1.name = Connection.location_a and location2.name = Connection.location_b
order by means_transport, way;

-- Show subset of locations based on batch number
select * from Location where Location.batch > 0 and Location.batch <= 20;
select * from Location where Location.batch = 2900 order by Location.name;

-- Shows number of locations inside provided geographic bounds
select count(name) from Location where latitude >= 39.0 and latitude <= 41.0 and longitude >= -5.0 and longitude <= -4.0;

-- Show locations ordered by length of respective names
select name, length(name) from Location order by length(name), name;

-- Show the number of connections of the Portuguese North Line assuming the longest route (Regional train, and Suburban train when available)
-- Connections must either belong to one of the 3 Portuguese Suburban train services, or to the Regional train services, without overlapping
-- For this, the suburban Azambuja Line and Aveiro Line must be excluded
-- Connections featuring the InterRegional train but not the Regional train should also be excluded
-- Part of the Coimbra Suburban trains do not run on a line with a dedicated name, so Regional train connections there must be excluded by hand
select count(location_a), sum(distance)
from Connection
where (way like '%Linha do Norte%') and
      ((way like '%CP Lisboa%') or (way like '%Urbanos de Coimbra%') or (way like '%CP Porto%') or
       (((way like '% Regional%') or (way like '%/Regional%'))
            and (way not like '%CP Lisboa%') and (way not like '%Urbanos de Coimbra%') and (way not like '%CP Porto%')
            and (way not like '%Linha da Azambuja%') and (way not like '%Linha de Aveiro%'))) and
    ((location_a != 'Estação de Espadaneira') and (location_b != 'Estação de Taveiro')) and
    ((location_a != 'Estação de Pereira') and (location_b != 'Estação de Taveiro'));
