default: zip_tasklib


zip_tasklib:
	tar -czvf sample_tasklib.tar.gz main_entity.py webserver.py tasklib

unzip_tasklib:
	mkdir unzip_tasklib && tar -xzvf sample_tasklib.tar.gz -C unzip_tasklib

clean:
	rm -rf unzip_tasklib
	rm sample_tasklib.tar.gz
