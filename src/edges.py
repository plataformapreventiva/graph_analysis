#!/usr/bin/env python
from __future__ import print_function
import re
import random
import boto3
import botocore
import smart_open
import csv
import numpy as np
from the_data import *
# session = boto3.Session(region_name='us-west-1')
# s3 = session.client('s3', config=botocore.client.Config(signature_version='s3v4'))

# FILENAME = 's3://pub-raw/nominal/2013/part-r-00000-02dbbed4-1b9e-4fa5-bf07-e57c7e9c50e9.csv'

EDGEH='s3://neo-nominal/data/edges/headers/'
EDGEL='s3://neo-nominal/data/edges/lists/'
TEMP ='s3://neo-nominal/data/tmp/'
the_id=re.compile(r'[0-9]{8}')
with smart_open.smart_open(TEMP+'periods.csv','w') as f2,\
smart_open.smart_open(TEMP+'payments.csv','w') as f3,\
smart_open.smart_open(TEMP+'errors.csv','w') as f4,\
smart_open.smart_open(EDGEH+'roll_person.csv','w') as h6,\
smart_open.smart_open(EDGEL+'roll_person.csv','w') as l6,\
smart_open.smart_open(EDGEH+'program_roll.csv','w') as h7,\
smart_open.smart_open(EDGEL+'program_roll.csv','w') as l7,\
smart_open.smart_open(EDGEH+'entity_municipality.csv','w') as h8,\
smart_open.smart_open(EDGEL+'entity_municipality.csv','w') as l8,\
smart_open.smart_open(EDGEH+'entity_roll.csv','w') as h9,\
smart_open.smart_open(EDGEL+'entity_roll.csv','w') as l9,\
smart_open.smart_open(EDGEH+'person_municipality.csv','w') as h10,\
smart_open.smart_open(EDGEL+'person_municipality.csv','w') as l10:
    with smart_open.smart_open('s3://pub-raw/concatenation/headers.csv','r') as r:
        reader = csv.reader(r,delimiter='|')
        for row in reader:
            h6.write(':START_ID|:END_ID|cd_beneficio|anio|nu_mes_pago|nu_imp_monetario|:TYPE|inicio|final')
            h7.write(':START_ID|:END_ID|:TYPE')
            h8.write(':START_ID|:END_ID|:TYPE')
            h9.write(':START_ID|:END_ID|:TYPE')
            h10.write(':START_ID|:END_ID|localidad|:TYPE|anio|nu_correspondencia')
    for FILENAME in FNAME:
        with smart_open.smart_open(FILENAME,'r') as r:
            reader = csv.reader(r, delimiter='|')
            for row in reader:
                # Cambiamos los periodos por una de inicio y fin
                row[6] = row[6].replace("_","|")
                row[6] = row[6].replace("A","10")
                row[6] = row[6].replace("B","11")
                row[6] = row[6].replace("C","12")
                # f2.write(row[6]+'\n')
                # Tomamos los datos de los pagos
                # payment1 = (str(row[5])+str(row[12]))[2:6]
                # payment2 = row[14]
                # f3.write((str(row[5])+str(row[12]))[2:6]+'|'+str(row[14])+'\n')
                    # if random.random() < 0.1:
                if re.match(the_id, row[16]) is not None and len(row)==23:
                    if row[16]!="":
                        l6.write('|'.join([row[4],row[16],row[22],row[5],row[14],row[17],'pago',row[6]])+'\n')
                    else:
                        l6.write('|'.join([row[4],'no-id',row[22],row[5],row[14],row[17],'pago',row[6]])+'\n')
                    if row[3] != "" and row[4] != "":
                        l7.write('|'.join([row[3],row[4],'pertenece'])+'\n')
                    if row[18] != "" and row[19] != "":
                        l8.write('|'.join([row[18],row[19],'pertenece'])+'\n')
                    if row[18] != "" and row[4] != "":
                        l9.write('|'.join([row[18],row[4],'pertenece'])+'\n')
                    if row[16] !="" and row[18] !="" and row[20] !="":
                        l10.write('|'.join([row[16],str(row[18])[2:],row[20],'vive',row[5],row[15]])+'\n')
