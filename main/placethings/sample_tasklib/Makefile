default: zip_tasklib


zip_tasklib:
	tar -czvf sample_tasklib.tar.gz main_entity.py webserver.py tasklib

unzip_tasklib:
	mkdir unzip_tasklib && tar -xzvf sample_tasklib.tar.gz -C unzip_tasklib

docker_build:
	sudo docker build --no-cache -t kumokay/heliot_host:$(TAG) .

docker_push:
	sudo docker push kumokay/heliot_host:$(TAG)

docker_pull:
	sudo docker pull kumokay/heliot_host:$(TAG)

clean:
	rm -rf unzip_tasklib
	rm sample_tasklib.tar.gz
