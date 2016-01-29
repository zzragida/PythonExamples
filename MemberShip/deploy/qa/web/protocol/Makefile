PYTHON=/usr/bin/python2.7
PROTOC=/usr/local/bin/protoc

all: protocol 


membership_pb2.py: membership.proto
	$(PROTOC) --python_out=../membership $<
	$(PROTOC) --python_out=../admin $<
	$(PROTOC) --python_out=../test $<

protocol: membership_pb2.py

clean:
	rm -f *_pb2.py *.pyc
