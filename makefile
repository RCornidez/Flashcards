# makefile
# run commands with:
# 		make [command] e.g. make install

# Install dependencies
install:
	pip install -r requirements.txt

# Run the Flask application
# Locally only on localhost
production:
	export FLASK_ENV=production
	flask run

# On all your network adapters so it's available on your network
development:
	export FLASK_ENV=development
	flask run --host 0.0.0.0 

# Run tests
test:
	python -m unittest discover -v tests

# Clean up pycache or other unwanted files
clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;
