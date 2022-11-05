## Railways in this project

Railways are one of the most important means of transport, and they have a strong presence in this project. Both Portugal and Spain have a large rail network, which is being covered here station by station.

### How railways are being covered

Active passenger lines are to be covered. Closed stations are being ignored, as are freight-only railways.

#### Locations

Locations are centered in each rail station, and most of the time have names with the format `<name of> Station` (usually `Estação de <name>` in Portuguese). Examples: Coimbra-B Station, Porto - Campanhã Station, Madrid-Atocha Station.

If the settlement where the station is located is to be covered as well, two solutions have been found: either the station location is converted into a location for the whole settlement (examples can be found in the Algarve Line), or the location for the settlement becomes a second separate location (example is Vilar Formoso in Portugal).

#### Connections

As railways frequently have multiple services operating on them, it was decided to consider both the railway itself and the service when creating connections.

Connections for railways have names with the format `<line 1>/<line 2>/... - <service 1>/<service 2>/...`. Examples: Algarve Line - Regional, North Line - Intercidades/InterRegional/Regional, Sintra Line/Azambuja Line - CP Lisbon.

Line names to consider are the names of the physical railways (ex: Cintura Line), and also the names of lines associated with suburban services running in pre-existing railways (ex: Aveiro Line, Azambuja Line). Multiple names can coexist in the same connection.

A station can have multiple connections for the same railway, even if in real life they would partially overlap. For example, the Alfa Pendular connection between Lisboa - Oriente (known in Portuguese as the *Gare do Oriente*) and Santarém overlaps with the suburban Azambuja Line.

What should not occur is to have two connections between the **same** stations, which is not supported. The exception is if one of the connections is by high-speed train and the other is by standard train, in which case this is accepted.

#### Ordering connections

As with roads and waterways, the order in which surrounding locations are listed is important to allow faster movement and to give the user the impression of travelling in a railway with an established route.

That is, as much as possible, the 1st and the 2nd options (not counting the exit option) should keep pointing at the same directions along the same railway. For example, in the North Line in Portugal, option 1 always points at the south towards Lisbon (the start of the line), and option 2 always points at the north towards Porto (the end of the line).

It was decided to always give priority to the services with the most stops, to encourage the user to travel through all stations and to present faster trains as shortcuts instead of as the main route. For example, if a station is served by suburban rail and by high-speed trains, the first destination options would point at suburban train connections.

It was also decided that a station is considered served by a service, within the context of this project, if in real life at least one train per day (or less) stops there. For example, if a certain service usually stops in stations A, B and C, but the night train also stops in station D, then station D is considered served as well by this service.

###### Practical example

For a practical example, let's look at the Coimbra-B Station, serving the city of Coimbra in Portugal. See service sorting by number of stops at section "Portugal" below.

Coimbra-B Station is in the North Line ("Linha do Norte" in Portuguese), meaning that its main direction is south-north. It is also served by most of the train services available in Portugal.

1. The service with the most stops is the suburban train ("Urbanos de Coimbra" - "Coimbra Suburban Trains"). Going south, the next station is Bencanta. Therefore, it is the option 1.
2. Heading north, there is no longer a suburban train service. Instead, there is the Regional service, which stops at most or all stations along an intercity route. The next station is Adémia, which is now the option 2.
3. Coimbra-B is served by the Lousã Branch Line ("Ramal da Lousã") as well. Since the main south-north direction along the North Line is now covered regarding suburban and regional trains, option 3 can go to the connection by both suburban and regional train to the Coimbra Station (Coimbra and Coimbra-B are two different stations)
4. Again in the North Line, towards south, the next station is Alfarelos, both with the faster InterRegional and with the even faster Intercidades (Intercity) trains. Therefore, option 4 goes to Alfarelos.
5. Heading north in the North Line, the next station is Pampilhosa, again by both InterRegional and Intercidades. Option 5 goes to Pampilhosa.
6. As the Lousã Branch Line has no further services, the North Line towards the south is again focused. The next station through the services Lusitânia Comboio Hotel and Sud Expresso is Pombal, which is assigned the option 6.
7. Towards the north, the same services head to Santa Comba Dão towards the Beira Alta Line (starting in Pampilhosa, north of Coimbra), so it is assigned the option 7.
8. Finally, through the high-speed service Alfa Pendular, the next station to the south is Pombal, which receives the option 1 in the high-speed train menu
9. Towards the north with the Alfa Pendular service, the next station is Aveiro, which receives the option 2 in the respective screen.

#### Destinations

Unlike for roads, destinations for railways are being introduced not from signs onsite, but by looking at the surrounding most relevant stations.

In particular, the line terminus towards a particular direction should be present, along with the closest relevant station. These include major stations, such as district and province capitals, and rail intersections where two or more railways meet.

In areas with suburban trains, the most important stations of the network can also be present at the same time, even if a bit further away, even if 10 or more destinations for the same direction accumulate.

#### High-speed trains

High-speed trains are present in this project as a separate means of transport, "High-Speed Train". The standard train uses the means of transport "Train".

They are the Alfa Pendular in Portugal, and the AVE in Spain.

### Portugal

Railways are present in all districts of Continental Portugal. Neither the Azores not the Madeira islands have railways.

CP (Comboios de Portugal - Trains of Portugal) is the state-owned company operating trains in Portugal.

Portugal has the following rail services, ordered by descending number of stops for the same route length:

- Suburban trains - Present in Lisbon (CP Lisbon), Coimbra (Coimbra Suburban Trains) and Porto (CP Porto). Fertagus operates as well the services between Setúbal and Lisbon, instead of CP.
- Regional - Present throughout the country (except in the South Line) and having no seat reservation, they serve relatively short (or not so short) intercity routes stopping at most or all stations
- InterRegional - A faster regional service, skipping some stations along the way
- Intercidades (Intercity) - The base long-distance train service, serving most of the country. In most routes, they feature reserved seating, different classes and snacks and drinks available aboard
- Sud Expresso / Lusitânia Comboio Hotel / Celta
  - The Sud Expresso and the Lusitânia Comboio (Train) Hotel are suspended services that until 2020 connected Lisbon with the Spanish-French border at Irún / Hendaye and with Madrid, respectively, during the night. The services have been included in this project due to their relevance. In Portugal, the two services use the same train, hence appear always together. They skip most Portuguese stations along the way.
  - The Celta train connects Porto and Vigo, in Spain. Skips most stops along the way. While it is paired with the Sud Expresso and the Lusitânia Comboio Hotel in terms of number of stops, it never overlaps with them.
- Alfa Pendular - The Portuguese high-speed train, capable of travelling over 220 km/h. Travels between Braga in the north and Faro in the south. Used to travel to Guimarães as well, close to Braga, and this too is included in this project.

### Spain

TBD

### Gibraltar and Andorra

Neither Gibraltar nor Andorra have railways.