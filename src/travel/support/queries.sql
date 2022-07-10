-- Auxiliary queries to get statistics from the database

-- Show number of connections by means of transport
select meio_transporte, count(meio_transporte) from ligacao group by meio_transporte
                                                            order by count(meio_transporte), meio_transporte;

-- Show number of connections by way
select info_extra, count(info_extra) from ligacao group by info_extra order by count(info_extra), info_extra;

-- Show number of destinations by appearance
select destino, count(destino) from destino group by destino order by count(destino), destino;

-- Show number of Portuguese locations by parish, municipality, district, intermunicipal entity and region, respectively
select freguesia, concelho, count(freguesia) from local_portugal group by freguesia, concelho
                                                                 order by count(freguesia), freguesia, concelho;
select concelho, count(concelho) from local_portugal group by concelho order by count(concelho), concelho;
select distrito, count(distrito) from local_portugal, concelho where local_portugal.concelho = concelho.concelho
                                                               group by distrito order by count(distrito);
select entidade_intermunicipal, count(entidade_intermunicipal) from local_portugal, concelho
                                                               where local_portugal.concelho = concelho.concelho
                                                               group by entidade_intermunicipal
                                                               order by count(entidade_intermunicipal), entidade_intermunicipal;
select regiao, count(regiao) from local_portugal, concelho where local_portugal.concelho = concelho.concelho
                                                           group by regiao order by count(regiao), regiao;

-- Show number of Spanish locations by district, municipality, comarca, province and autonomous community, respectively

select distrito, municipio, count(distrito) from local_espanha where distrito is not null
                                                               group by distrito, municipio
                                                               order by count(distrito), municipio, distrito;

select municipio, count(municipio) from local_espanha group by municipio order by count(municipio), municipio;

select comarca, municipio.provincia, count(comarca)
from comarca, municipio, local_espanha
where comarca.municipio = municipio.municipio and local_espanha.municipio = municipio.municipio
group by comarca, municipio.provincia
order by count(comarca), municipio.provincia, comarca;

select provincia, count(provincia) from local_espanha group by provincia order by count(provincia), provincia;

select comunidade_autonoma, count(comunidade_autonoma)
from local_espanha, municipio, provincia
where local_espanha.municipio = municipio.municipio and municipio.provincia = provincia.provincia
group by comunidade_autonoma
order by count(comunidade_autonoma), comunidade_autonoma;

-- Show number of locations by protected area
select info_extra, count(info_extra) from local group by info_extra order by count(info_extra), info_extra;

-- Show number of Portuguese, Spanish and Gibraltar locations, respectively
select count(nome) as "Locations in Portugal" from local_portugal;
select count(nome) as "Locations in Spain" from local_espanha;
select count(nome) as "Locations in Gibraltar" from local_gibraltar;

-- Order locations by altitude, latitude and longitude, respectively
select nome, altitude from local order by altitude, nome;
select nome, latitude from local order by latitude, nome;
select nome, longitude from local order by longitude, nome;

-- Show locations with max and min latitude, longitude and altitude
select nome, latitude, longitude from local where latitude = (select max(latitude) from local);
select nome, latitude, longitude from local where latitude = (select min(latitude) from local);
select nome, latitude, longitude from local where longitude = (select min(longitude) from local);
select nome, latitude, longitude from local where longitude = (select max(longitude) from local);
select nome, latitude, longitude, altitude from local where altitude = (select max(altitude) from local);

-- Show connections featuring destinations, by number of destinations. Directions are shown separatedly
-- Ex: (Lisbon -> Oporto and Oporto -> Lisbon appear separatedly)
select destino.local_a, destino.local_b, destino.origem, destino.meio_transporte, ligacao.info_extra, count(*)
from destino, ligacao
where destino.local_a = ligacao.local_a and destino.local_b = ligacao.local_b and destino.meio_transporte = ligacao.meio_transporte
group by destino.local_a, destino.local_b, destino.origem, destino.meio_transporte, ligacao.info_extra
order by count(*), destino.local_a, destino.local_b, destino.origem, destino.meio_transporte, ligacao.info_extra;

-- Show ways by total length of connections associated to each way
select info_extra, sum(distancia), count(distancia) from ligacao group by info_extra order by sum(distancia), info_extra;

-- Show total length and number of connections associated to A-7 (Autovía del Mediterráneo) and AP-7 (Autopista del Mediterráneo)
select sum(distancia) as "Total distance of A-7 and AP-7", count(distancia) as "Number of connections of A-7 and AP-7"
from ligacao
where (info_extra like '%A-7%' or info_extra like '%AP-7%');

-- Show ways by total number of destinations associated to connections of each way
-- Destination names may appear repeatedly (ex: Lisbon and Oporto are destinations associated to virtually all connections of A1)
select info_extra, count(destino)
from destino, ligacao
where destino.local_a = ligacao.local_a and destino.local_b = ligacao.local_b and destino.meio_transporte = ligacao.meio_transporte
group by info_extra
order by count(destino), info_extra;

-- Show connection info associated with coordinates of locations
select local1.latitude, local1.longitude, local2.latitude, local2.longitude, ligacao.info_extra, ligacao.meio_transporte
from local as local1, local as local2, ligacao
where local1.nome = ligacao.local_a and local2.nome = ligacao.local_b
order by meio_transporte, info_extra;

-- Show subset of locations based on batch number
select * from local where local.lote > 0 and local.lote <= 20;

-- Shows number of locations inside provided geographic bounds
select count(nome) from local where latitude >= 39.0 and latitude <= 41.0 and longitude >= -5.0 and longitude <= -4.0;