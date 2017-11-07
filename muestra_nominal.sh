#!/usr/bin/env bash
aws s3api get-object --bucket pub-raw --key nominal/2013/part-r-00000-02dbbed4-1b9e-4fa5-bf07-e57c7e9c50e9.csv --range bytes=0-10000000 data/nominal-2013.csv
aws s3api get-object --bucket pub-raw --key nominal/2014/part-r-00000-5a4b3b26-6e87-4400-aae6-f921bfb78c8d.csv --range bytes=0-10000000 data/nominal-2014.csv
aws s3api get-object --bucket pub-raw --key nominal/2015/part-r-00000-4d33350f-3835-47bd-9eeb-dbf5cdfd82ae.csv --range bytes=0-10000000 data/nominal-2015.csv
aws s3api get-object --bucket pub-raw --key nominal/2016/part-r-00000-d27cf049-19fa-43ce-9286-f8815cbe2499.csv --range bytes=0-10000000 data/nominal-2016.csv

for year in {2013..2016};do
    sed -i '$ d' data/nominal-$year.csv
done
