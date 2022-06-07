#!/bin/bash

#Reseting file
echo >| src/convert.min.py

#Putting configs in file
echo -e '\n#################### Configurations ####################\n' >> src/convert.min.py && 
echo -n 'config = ' >> src/convert.min.py && 
cat src/config.json >> src/convert.min.py && 
sed -i 's/true/True/g' src/convert.min.py && 
echo -e '\n' >> src/convert.min.py &&
echo -e '\n✅️ Configurations parsed!' || 
echo -e '\n❌️ Error parsing Configurations!'

#Putting utils in file
echo -e '\n#################### Utils ####################\n' >> src/convert.min.py && 
cat src/utils.py >> src/convert.min.py && 
echo -e '\n' >> src/convert.min.py &&
echo -e '\n✅️ Utils parsed!' || 
echo -e '\n❌️ Error parsing Utils!'

#Putting main in file
echo -e '\n#################### Converter ####################\n' >> src/convert.min.py && 
tail -n +2 src/convert.py >> src/convert.min.py && 
echo -e '\n' >> src/convert.min.py &&
echo -e '\n✅️ Converter parsed!' || 
echo -e '\n❌️ Error parsing Converter!'

echo -e '\n'

#Test run
python3 src/convert.min.py && 
echo -e '\n✅️ Converter test run completed successfully!' || 
echo -e '\n❌️ Error Converter test run failed!'