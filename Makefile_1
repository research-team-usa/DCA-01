up:
	docker-compose up --build

down:
	docker-compose down

test:
	python -m pytest tests/ -v

lint:
	python -m jsonschema -i schemas/router_output_v1.json schemas/router_output_v1.json || true

schemas-validate:
	for f in schemas/*.json; do echo "Validating $$f"; python -m json.tool $$f > /dev/null; done
