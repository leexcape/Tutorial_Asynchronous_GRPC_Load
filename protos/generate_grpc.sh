#!/bin/bash

# generate the gRPC files from proto
python -m grpc_tools.protoc \
  -Igrpc_utils/test=. \
  --python_out=.. \
  --pyi_out=.. \
  --grpc_python_out=.. \
  grpc.proto

# Tips: To avoid the situation that generated _pb2 file can't be imported correctly by _pb2_grpc file, the path between
#       -I and = is appended after the output path, and this new combined path should be able to be tracked by python
#       from the root directory of the project. Specifically, the path between -I and = is the *** appears in the
#       "from *** import _pb2.py" in the _pb2_grpc file, and the actual output path is specified "--python_out" appended
#       by the path between -I and =. Also, the path after the = should be the place where .proto file is stored. So, a
#       better practice would be leaving "--python_out" path as the root path of the project.