deploy:
	make pypi_upload
	git push

pypi_upload:
	python setup.py sdist upload -r pypi || echo 'docker-emperor is up-to-date'

develop:
	sudo pip install .
	python setup.py develop --user
	which de
	which docker-emperor


undevelop:
	sudo pip uninstall docker-emperor
	sudo pip uninstall docker-emperor
	rm $(which de)
	rm $(which docker-emperor)
	
clean:
	find . -type f -name "*.pyc" -delete
	rm -rf nosetests.xml coverage.xml htmlcov *.egg-info *.pdf dist violations.txt





