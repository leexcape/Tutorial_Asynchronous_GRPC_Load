import grpc
from grpc_utils.test import grpc_pb2_grpc, grpc_pb2
import os, time, psutil
from concurrent import futures

REQUESTS_IN_FLIGHT = 0


class Servicer(grpc_pb2_grpc.BenchServicer):

    def Submit(self, request, context):
        global REQUESTS_IN_FLIGHT
        REQUESTS_IN_FLIGHT += 1
        # ─── 模拟 I/O ───
        time.sleep(0.5)
        REQUESTS_IN_FLIGHT -= 1
        return grpc_pb2.Empty()


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_pb2_grpc.add_BenchServicer_to_server(Servicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()

    # 每秒打印监控
    proc = psutil.Process(os.getpid())
    while True:
        time.sleep(0.5)
        print(f"threads={proc.num_threads():2d} "
              f"inflight={REQUESTS_IN_FLIGHT:5d}")


if __name__ == "__main__":
    proc = psutil.Process(os.getpid())
    print(f"threads={proc.num_threads():2d} "
          f"inflight={REQUESTS_IN_FLIGHT:5d}")
    print("start!!!!!!")
    main()

