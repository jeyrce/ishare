
image:=jeyrce/ishare:v1.0.3-final

.phony: all
all:
	docker buildx create --use
	docker buildx build -t ${image} \
		--platform=linux/amd64 \
		--pull \
		--push \
		.

