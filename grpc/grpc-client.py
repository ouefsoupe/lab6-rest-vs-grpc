import argparse, time, statistics, random, base64, grpc
from pathlib import Path
import lab6_pb2 as pb, lab6_pb2_grpc as pbg

def bench(fn, reps):
    ts=[]
    for _ in range(reps):
        t0=time.perf_counter(); fn(); ts.append((time.perf_counter()-t0)*1000)
    return {
        "avg_ms": sum(ts)/len(ts),
        "reps": len(ts)
    }

def main():
    ap = argparse.ArgumentParser()
    # flag-style
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=50051)
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--vec", type=int, default=100)
    ap.add_argument("--image", default="../Flatirons_Winter_Sunrise_edit_2.jpg")
    ap.add_argument("--which", choices=["add","rawimg","dot","jsonimg","all"], default="all")
    # positional-style (optional)
    ap.add_argument("pos_host", nargs="?", help="host or host:port (positional)")
    ap.add_argument("pos_cmd", nargs="?", help="add | rawImage | dotProduct | jsonImage (positional)")
    ap.add_argument("pos_reps", nargs="?", type=int, help="repetitions (positional)")
    args = ap.parse_args()

    # If user used positional args, map them into flags
    if args.pos_host:
        h = args.pos_host
        if ":" in h:
            host, port = h.split(":", 1)
            args.host = host
            try: args.port = int(port)
            except: pass
        else:
            args.host = h
    if args.pos_cmd:
        # accept several spellings/cases
        m = args.pos_cmd.strip().lower()
        alias = {"rawimage":"rawimg", "jsonimage":"jsonimg", "dotproduct":"dot", "add":"add"}
        args.which = alias.get(m, m)
    if args.pos_reps is not None:
        args.reps = args.pos_reps

    chan = grpc.insecure_channel(f"{args.host}:{args.port}")
    stub = pbg.Lab6Stub(chan)
    print(f"Target: {args.host}:{args.port}  reps={args.reps}")

    def show(name, res): print(f"{name}: {res['avg_ms']:.3f} ms/op (n={res['reps']})")

    # helpers
    raw_bytes = Path(args.image).read_bytes()
    b64 = base64.b64encode(raw_bytes).decode("ascii")

    if args.which in ("add","all"):
        show("gRPC add", bench(lambda: stub.Add(pb.AddRequest(a=5,b=10)), args.reps))
    if args.which in ("rawimg","all"):
        show("gRPC rawimg", bench(lambda: stub.RawImage(pb.ImageRequest(image=raw_bytes)), max(10, args.reps)))
    if args.which in ("dot","all"):
        def once():
            a=[random.random() for _ in range(args.vec)]
            b=[random.random() for _ in range(args.vec)]
            stub.DotProduct(pb.DotRequest(a=a,b=b))
        show("gRPC dot", bench(once, max(50, args.reps)))
    if args.which in ("jsonimg","all"):
        show("gRPC jsonimg", bench(lambda: stub.JsonImage(pb.JsonImageRequest(image_b64=b64)), max(10, args.reps)))

if __name__ == "__main__":
    main()
