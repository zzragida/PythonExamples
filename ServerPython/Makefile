PYTHON=/usr/bin/python2.7
PROTOC=/usr/local/bin/protoc


PROTOCOL_PATH=/home/kjs/projects/M3ARPG/Server/src/protocol

all: protocol 

protocol/common_pb2.py: $(PROTOCOL_PATH)/common.proto
	$(PROTOC) --proto_path=$(PROTOCOL_PATH) --python_out=protocol $<

protocol/gateway_pb2.py: $(PROTOCOL_PATH)/gateway.proto
	$(PROTOC) --proto_path=$(PROTOCOL_PATH) --python_out=protocol $<

protocol/room_pb2.py: $(PROTOCOL_PATH)/room.proto
	$(PROTOC) --proto_path=$(PROTOCOL_PATH) --python_out=protocol $<

protocol/stage_pb2.py: $(PROTOCOL_PATH)/stage.proto
	$(PROTOC) --proto_path=$(PROTOCOL_PATH) --python_out=protocol $<



protocol: protocol/common_pb2.py protocol/room_pb2.py protocol/gateway_pb2.py protocol/stage_pb2.py

clean:
	rm -f protocol/*_pb2.py protocol/*.pyc
