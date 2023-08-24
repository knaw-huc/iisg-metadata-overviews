echo "Start ORCID cetl-pipeline"
echo "-----"
echo "Remove old stuff"
rm -r extracted/

echo "-----"
echo "Extract data"
./extractor.py

echo "-----"
echo "Compress data"
zip -r orcid.zip extracted/
mv orcid.zip extracted/

echo "-----"
echo "Ready"