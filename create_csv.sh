#!/usr/bin/env bash

export DATA=./data
export NODEH=./data/nodes/headers
export NODEL=./data/nodes/list
export EDGEH=./data/edges/headers
export EDGEL=./data/edges/list
export TEMP=./data/temp

[ -d $NODEH ] || mkdir -p $NODEH
[ -d $NODEL ] || mkdir -p $NODEL
[ -d $EDGEH ] || mkdir -p $EDGEH
[ -d $EDGEL ] || mkdir -p $EDGEL
[ -d $TEMP  ] || mkdir -p $TEMP

for year in {2013..2016};do

# Cambiamos la columna periodo por una de inicio y una de fin
awk 'BEGIN {FS="|"}NR!=1{print$7}' $DATA/nominal-$year.csv | tr '_' '|' | sed 's/C/12/g;s/B/11/g;s/A/10/g' \
 > $TEMP/periods.csv


# Hacemos la nueva columna de POSIX
paste -d"|" <(awk 'BEGIN {FS="|"}NR!=1{print $21}' $DATA/nominal-$year.csv) <(awk 'BEGIN {FS="|"}NR!=1{print $21}' $DATA/nominal-$year.csv | awk -v OFS='|' '{cmd="date -d \""$1"\" +%s"; cmd | getline $1; close(cmd)} 1') > $TEMP/dates.csv

# Tomamos los datos de los pagos
paste -d"|" <(awk '{FS="|"}NR!=1{print $6$13}' $DATA/nominal-$year.csv | awk '{print substr($0,3,6)}') <(awk '{FS="|"}NR!=1{print $15}' $DATA/nominal-$year.csv) \
    > $TEMP/payments.csv

# Nodo PERSONA
awk 'BEGIN {FS="|"}NR==1{print"nombre|"$12"|"$14":ID|"$23"|"$21"|posix"}' $DATA/nominal-$year.csv > $NODEH/person.csv
paste -d"|" <(awk 'BEGIN {FS="|"}NR!=1{if ($12!=""){print$8" "$9" "$10"|"$12"|"$14"|"$23} else {print$8" "$9" "$10"|indefinido|"$14"|"$23}}' $DATA/nominal-$year.csv) \
    <(cat $TEMP/dates.csv) | sort -k 3 -t$'|' -u >> $NODEL/person.csv

# Nodo ENTIDAD
echo 'State:ID' > $NODEH/state.csv
awk 'BEGIN {FS="|"}NR!=1{print$16}' $DATA/nominal-$year.csv | sort -u >> $NODEL/state.csv

# Nodo Municipio
echo 'municipality:ID' > $NODEH/municipality.csv
awk 'BEGIN {FS="|"}NR!=1{print $24"m"}' $DATA/nominal-$year.csv | sort -u >> $NODEL/municipality.csv

# Nodo Programa
echo 'cd:ID' > $NODEH/program.csv
awk 'BEGIN {FS="|"}NR!=1{print $4"p"}' $DATA/nominal-$year.csv | sort -u >> $NODEL/program.csv

# Nodo Padron
echo 'cd:ID' > $NODEH/roll.csv
awk 'BEGIN {FS="|"}NR!=1{print $5}' $DATA/nominal-$year.csv | sort -u >> $NODEL/roll.csv

# Arista PADRON-PERSONA
echo ':START_ID|:END_ID|beneficio:int|fecha:int|importe:float|:TYPE|inicio:int|final:int' > $EDGEH/roll_person.csv
paste -d"|" <(awk 'BEGIN {FS="|"}NR!=1{if($14!=""){print $5"|"$14"|"$20} else {print $5"|no-id|"$20}}' $DATA/nominal-$year.csv)\
    <(awk 'BEGIN {FS="|"}{print $1"|"$2"|pago"}' $TEMP/payments.csv) <(cat $TEMP/periods.csv) | sed '$ d' >> $EDGEL/roll_person.csv

# Arista PROGRAMA-PADRON
echo ':START_ID|:END_ID|:TYPE' > $EDGEH/program_roll.csv
awk 'BEGIN {FS="|"}NR!=1{print $5"|"$4"p|pertenece"}' $DATA/nominal-$year.csv | sort -u | sed '$ d' >> $EDGEL/program_roll.csv

# Arista ENTIDAD-MUNICIPIO
echo ':START_ID|:END_ID|:TYPE' > $EDGEH/entity_municipality.csv
awk 'BEGIN {FS="|"}NR!=1{print $24"m|"$16"|pertenece"}' $DATA/nominal-$year.csv | sort -u | sed '$ d' >> $EDGEL/entity_municipality.csv

# Arista ESTADO-PADRON
echo ':START_ID|:END_ID|:TYPE' > $EDGEH/state_roll.csv
awk 'BEGIN {FS="|"}NR!=1{print $24"m|"$5"|pertenece"}' $DATA/nominal-$year.csv | sort -u | sed '$ d' >> $EDGEL/state_roll.csv

# Arista MUNICIPIO-PERSONA
echo ':START_ID|:END_ID|localidad|:TYPE|fecha' > $EDGEH/person_municipality.csv
paste -d"|" <(awk 'BEGIN {FS="|"}NR!=1{print $14"|"$24"m|"$18"|vive"}' $DATA/nominal-$year.csv) <(awk 'BEGIN {FS="|"}{print $1}' $TEMP/payments.csv) | sort -u | sed '$ d' >> $EDGEL/person_municipality.csv
rm -r $TEMP/*
done
cp $NODEL/person.csv $TEMP/person.csv
cp $NODEL/municipality.csv $TEMP/municipality.csv
cp $NODEL/state.csv $TEMP/state.csv
cp $NODEL/roll.csv $TEMP/roll.csv
sort -u $TEMP/person.csv > $NODEL/person.csv
sort -u $TEMP/municipality.csv > $NODEL/municipality.csv
sort -u $TEMP/state.csv > $NODEL/state.csv
sort -u $TEMP/roll.csv > $NODEL/roll.csv
rm -r $TEMP/*
