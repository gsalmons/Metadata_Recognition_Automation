# Build the Docker image
docker build -t srp33/trial1 .

# Run the Docker container with volume mounts
# docker run -d --rm \
docker run --rm -i -t \
    -v $(pwd)/bioProjectIds:/bioProjectIds/ \
    -v $(pwd)/scripts:/scripts/ \
    -v $(pwd)/results:/results/ \
    -v $(pwd)/models:/models/ \
    -v $(pwd)/predictions:/predictions/ \
    -v $(pwd)/bioSamples:/bioSamples/ \
    srp33/trial1 \
    /exec_analysis.py