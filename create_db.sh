#! /usr/bin/env bash

export NODEH=./data/nodes/headers
export NODEL=./data/nodes/list
export EDGEH=./data/edges/headers
export EDGEL=./data/edges/list
/var/lib/neo4j/bin/neo4j-admin import --mode=csv --delimiter="|" \
    --database=nominal.db \
    --ignore-duplicate-nodes=true \
    --nodes:person "$NODEH/person.csv,$NODEL/person.csv" \
    --nodes:state "$NODEH/state.csv,$NODEL/state.csv" \
    --nodes:municipality "$NODEH/municipality.csv,$NODEL/municipality.csv" \
    --nodes:program "$NODEH/program.csv,$NODEL/program.csv" \
    --nodes:roll "$NODEH/roll.csv,$NODEL/roll.csv" \
    --relationships "$EDGEH/roll_person.csv,$EDGEL/roll_person.csv" \
    --relationships "$EDGEH/program_roll.csv,$EDGEL/program_roll.csv" \
    --relationships "$EDGEH/entity_municipality.csv,$EDGEL/entity_municipality.csv" \
    --relationships "$EDGEH/state_roll.csv,$EDGEL/state_roll.csv" \
    --relationships "$EDGEH/person_municipality.csv,$EDGEL/person_municipality.csv" \
