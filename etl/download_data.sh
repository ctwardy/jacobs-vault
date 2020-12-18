#!/bin/bash

# This script downloads the original AIS and TLE data for the challenge from S3

# Download AIS data

currdir=TLE
mkdir $currdir

wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2015_01_Zone01.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2015_01_Zone02.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2015_01_Zone03.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2016_01_Zone01.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2016_01_Zone02.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2016_01_Zone03.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2017_01_Zone01.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2017_01_Zone02.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/AIS_2017_01_Zone03.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/Zone10_2009_01.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/Zone10_2010_01.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/Zone10_2011_01.gdb.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/Zone10_2012_01.gdb.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/Zone10_2013_01.gdb.zip
wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/AIS/Zone10_2014_01.zip.wzd

# Download TLE data

currdir=TLE
mkdir $currdir

for i in {1..8}
do
	wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/TLE/tle2004_${i}of8.txt.zip
done

for i in {2005..2018}
do
	wget --directory-prefix=${currdir} https://afdata.s3-us-gov-west-1.amazonaws.com/Scenario_Data/TLE/tle${i}.txt.zip
done