#!/usr/bin/env python

# from __future__ import print_function
import smart_open
import csv
import re
import numpy as np
import time
import datetime
from the_data import *

# FILENAME = 's3://pub-raw/nominal/2013/part-r-00000-02dbbed4-1b9e-4fa5-bf07-e57c7e9c50e9.csv'

counter = 0
NODEH='s3://neo-nominal/data/nodes/headers/'
NODEL='s3://neo-nominal/data/nodes/lists/'
TEMP ='s3://neo-nominal/data/tmp/'
the_id=re.compile(r'[0-9]{8}')
with smart_open.smart_open(TEMP+'periods.csv','w') as f2,\
smart_open.smart_open(TEMP+'payments.csv','w') as f3,\
smart_open.smart_open(TEMP+'errors.csv','w') as f4,\
smart_open.smart_open(NODEH+'person2.csv','w') as h1,\
smart_open.smart_open(NODEL+'person2.csv','w') as l1,\
smart_open.smart_open(NODEH+'state.csv','w') as h2,\
smart_open.smart_open(NODEL+'state.csv','w') as l2,\
smart_open.smart_open(NODEH+'municipality.csv','w') as h3,\
smart_open.smart_open(NODEL+'municipality.csv','w') as l3,\
smart_open.smart_open(NODEH+'program.csv','w') as h4,\
smart_open.smart_open(NODEL+'program.csv','w') as l4,\
smart_open.smart_open(NODEH+'roll.csv','w') as h5,\
smart_open.smart_open(NODEL+'roll.csv','w') as l5:
    seen_person= set()
    seen_state= set()
    seen_municipality= set()
    seen_program= set()
    seen_roll= set()
    for FILENAME in FNAME:
        with smart_open.smart_open(FILENAME,'r') as r:
            # f = (line.decode('utf-8') for line in r)
            reader = csv.reader(r, delimiter='|')
            for row in reader:
                # Cambiamos los periodos por una de inicio y fin
                row[6] = row[6].replace("_","|")
                row[6] = row[6].replace("A","10")
                row[6] = row[6].replace("B","11")
                row[6] = row[6].replace("C","12")
                f2.write(row[6]+'\n')
                # Tomamos los datos de los pagos
                payment = (str(row[5])+str(row[12]))[2:6]+'|'+str(row[14])
                try:
                    bday = row[20]
                    date_posix = int(time.mktime(datetime.datetime.strptime(bday, "%Y-%m-%d").timetuple()))
                except:
                    d = datetime.datetime.now()
                    date_posix = int(time.mktime(d.timetuple()))
                    # f4.write(bday+'\n')
                # f3.write((str(row[5])+str(row[12]))[2:6]+'|'+str(row[14])+'\n')
                if counter == 0:
                    # Nodos
                    h1.write('|'.join(["paterno","materno","nombres",row[11],row[13]+":ID",row[22],row[20],"posix"]))
                    h2.write('State:ID')
                    h3.write('Municipality:ID')
                    h4.write('cd:ID')
                    h5.write('cd:ID')
                    counter += 1
                else:
                    if re.match(the_id, row[13]) is not None and len(row)==25:
                        if row[13] not in seen_person:
                            seen_person.add(row[13])
                            if row[13]=="":
                                iden = "no-id"
                            else:
                                iden = row[13]
                            if row[11]=="":
                                l1.write('|'.join([row[7],row[8],\
                                        row[9],"indefinido",iden,\
                                        row[22],bday,str(date_posix)])+'\n')
                            else:
                                l1.write('|'.join([row[7],row[8],\
                                        row[9],row[11],iden,\
                                        row[22],bday,str(date_posix)])+'\n')
                        if row[15] not in seen_state:
                            seen_state.add(row[15])
                            l2.write(row[15]+'\n')
                        try:
                            muni = str(row[23])
                            if muni not in seen_municipality:
                                seen_municipality.add(muni)
                                l3.write(muni+'\n')
                        except:
                            muni = str(0)
                            seen_municipality.add(muni)
                            l3.write(muni+'\n')
                        if row[3] not in seen_program:
                            seen_program.add(row[3])
                            l4.write(row[3]+'\n')
                        if row[4] not in seen_roll:
                            seen_roll.add(row[4])
                            l5.write(row[4]+'\n')
