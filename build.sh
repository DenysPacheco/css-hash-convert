#!/bin/bash

#Reseting file
echo >| convert.min.py

#Putting configs in file
echo -e '\n#################### Configurations ####################\n' >> convert.min.py && 
echo -n 'config = ' >> convert.min.py && 
cat config.json >> convert.min.py && 
sed -i 's/true/True/g' convert.min.py && 
echo -e '\n' >> convert.min.py &&
echo -e '\n✅️ Configurations parsed!' || 
echo -e '\n❌️ Error parsing Configurations!'

#Putting functions in file
echo -e '\n#################### Functions ####################\n' >> convert.min.py && 
cat functions.py >> convert.min.py && 
echo -e '\n' >> convert.min.py &&
echo -e '\n✅️ Functions parsed!' || 
echo -e '\n❌️ Error parsing Functions!'

#Putting main in file
echo -e '\n#################### Converter ####################\n' >> convert.min.py && 
cat convert.py >> convert.min.py && 
echo -e '\n' >> convert.min.py &&
echo -e '\n✅️ Converter parsed!' || 
echo -e '\n❌️ Error parsing Converter!'