import asyncio, grpc, uuid
from grpc_utils.test import grpc_pb2_grpc, grpc_pb2
import os, time, psutil
from redis import asyncio as aioredis

REQUESTS_IN_FLIGHT = 0
redis = aioredis.from_url("redis://localhost:6379/0", decode_responses=False)

class Servicer(grpc_pb2_grpc.BenchServicer):

    async def Submit(self, request, context):
        global REQUESTS_IN_FLIGHT
        REQUESTS_IN_FLIGHT += 1
        job_id = uuid.uuid4().hex
        try:
            # print("⇢ start", request)  # 入口
            # await asyncio.sleep(0.075)  # 模拟 I/O
            await redis.lpush("inference:tasks", job_id)
            # print("⇠ normal end")
            return grpc_pb2.Empty()
        except asyncio.CancelledError:
            print("⚠ got CancelledError")  # client 程序结束也会在这里触发cancel
            raise
        finally:
            REQUESTS_IN_FLIGHT -= 1  # 始终执行
        return grpc_pb2.Empty()


async def main():
    server = grpc.aio.server()
    grpc_pb2_grpc.add_BenchServicer_to_server(Servicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()

    loop = asyncio.get_running_loop()
    loop.set_debug(True)                     # 打开事件循环 lag 监控

    # 每秒打印监控
    proc = psutil.Process(os.getpid())
    while True:
        await asyncio.sleep(0.5)
        print(f"threads={proc.num_threads():2d} "
              f"inflight={REQUESTS_IN_FLIGHT:5d}")
    await server.wait_for_termination()

if __name__ == "__main__":
    proc = psutil.Process(os.getpid())
    print(f"threads={proc.num_threads():2d} "
          f"inflight={REQUESTS_IN_FLIGHT:5d}")
    print("start!!!!!")
    asyncio.run(main())