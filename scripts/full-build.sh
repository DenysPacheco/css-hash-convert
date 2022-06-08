echo -e 'Cleaning...\n' &&

rm -rfv examples/*.min*; rm -rfv examples/*/*.min*; rm -rfv __pycache__/ .pytest_cache/; rm tempCodeRunnerFile.py &&

scripts/del_pycache.sh;

echo -e 'Starting Full build...\n' &&

echo -e 'Testing...\n' &&

pytest &&

echo -e 'Build convert.min.py...' &&

scripts/build.sh &&

echo -e 'Making docs...\n' &&

sphinx-apidoc -fo docs/source/ src/ && cd docs && make html &&

echo -e '\nFull build complete!'