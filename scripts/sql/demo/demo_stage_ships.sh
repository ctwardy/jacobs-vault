#!/bin/bash
#  Split out ships by year and mmsi for demo
for i in 2015 2016 2017
do
   ./demo_stage_ships_.sh $i &
done 
