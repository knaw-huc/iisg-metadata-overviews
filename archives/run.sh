echo "Start archives cetl-pipeline"
echo "-----"

echo "-----"
echo "Monitor data"
./extractor.py

echo "-----"
echo "Extract data"
./extractor.py

echo "-----"
echo "Transform data"
./transformer.py

echo "-----"
echo "Compress data"
zip -r archives.zip extracted/
mv orcid.zip extracted/

echo "-----"
echo "Ready"