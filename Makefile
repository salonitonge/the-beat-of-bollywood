.PHONY: run web clean

run:
	python3 scripts/clean_and_analyze.py

web:
	cd web && python3 -m http.server 8000

clean:
	rm -rf data/cleaned/* web/story_data.json
