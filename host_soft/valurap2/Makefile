image: Dockerfile
	docker build --platform armhf -f Dockerfile.base -t valurap-base:latest .
	docker build --platform armhf -f Dockerfile -t valurap:latest .

TAG := $(shell date "+%Y%m%d-%H%M%S")

image-push:
	docker tag valurap:latest ghcr.io/sevikkk/valurap:${TAG}
	docker push ghcr.io/sevikkk/valurap:${TAG}

constraints.txt: image
	docker run --rm valurap:latest pip freeze --exclude-editable >constraints.txt 
