use vault;

create table AIS_raw
(
	MMSI string,
	BaseDateTime string,
	LAT string,
	LON string,
	SOG string,
	COG string,
	Heading string,
	VesselName string,
	IMO string,
	CallSign string,
	VesselType string,
	Status string,
	Length string,
	Width string,
	Draft string,
	Cargo string
)

row format delimited
fields terminated by ",";


