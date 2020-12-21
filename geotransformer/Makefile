# Create/compress a local conda environment and compress the botlife directory
build:
	conda env create -p environment --file environment.yml
	zip -r environment.zip environment
	zip -r geotransformer.zip geotransformer
	
# Update environment.yml dependencies without recreating the environment
reinstall:
	conda env update -p environment --file environment.yml
	# The zip program returns error code 12 when there is nothing to update
	zip -u -r environment.zip environment

# Update the botlife archive with any changes made to the botlife directory
update:
	# The zip program returns error code 12 when there is nothing to update
	rm -f geotransformer.zip
	zip -r geotransformer.zip geotransformer

# Remove the environment directory and all archives in order to start fresh
clean:
	rm -rf environment
	rm -f environment.zip
	rm -r geotransformer.zip

