#!/usr/bin/env python3
import io, base64, grpc
from concurrent import futures
from PIL import Image

import lab6_pb2 as pb
import lab6_pb2_grpc as pbg

class Lab6Servicer(pbg.Lab6Servicer):
    def Add(self, req, ctx):
        return pb.AddReply(sum=req.a + req.b)

    def RawImage(self, req, ctx):
        img = Image.open(io.BytesIO(req.image))
        w, h = img.size
        return pb.ImageReply(width=w, height=h)

    def DotProduct(self, req, ctx):
        if len(req.a) != len(req.b):
            ctx.abort(grpc.StatusCode.INVALID_ARGUMENT, "vectors must be same length")
        dot = sum(float(x) * float(y) for x, y in zip(req.a, req.b))
        return pb.DotReply(dot=dot)

    def JsonImage(self, req, ctx):
        raw = base64.b64decode(req.image_b64, validate=True)
        img = Image.open(io.BytesIO(raw))
        w, h = img.size
        return pb.ImageReply(width=w, height=h)

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    pbg.add_Lab6Servicer_to_server(Lab6Servicer(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server listening on :50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()
