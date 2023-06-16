echo "Start ORCID cetl-pipeline"
echo "-----"
echo "Remove old stuff"
rm status.db
rm -r extracted/

echo "-----"
echo "Build database and check identifiers"
./00_check.py

echo "-----"
echo "Extract data"
./10_extract.py
./15_extract_statusupdate.py

echo "-----"
echo "Compress data"
zip -r orcid.zip extracted/
mv orcid.zip extracted/

echo "-----"
echo "Ready"