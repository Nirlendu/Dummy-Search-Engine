all:
	sudo apt-get install tornado
	python Crawler_Indexer.py
	python Search.py
