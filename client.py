import grpc, threading, time
from grpc_utils.test import grpc_pb2_grpc, grpc_pb2

CH = grpc.insecure_channel("localhost:50051")
stub = grpc_pb2_grpc.BenchStub(CH)
lst = []
def bombard(n):
    for _ in range(n):
        fut = stub.Submit.future(grpc_pb2.Empty())   # 异步 Future，不等结果
        lst.append(fut)  # 还是要处理一下结果，不然server直接取消

workers = []
start = time.perf_counter()
for _ in range(2000):                 # 200 × 10 = 2 000 RPC
    t = threading.Thread(target=bombard, args=(10,))
    t.start()
    workers.append(t)

for t in workers: t.join()
took = time.perf_counter() - start
print(f"sent 2k requests in {took:.2f}s")
