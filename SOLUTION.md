
|  Method 	        | Local | Same-Zone |  Different Region 	|
|---	            |---	|---	    |---	                |---	|
|   REST add        | 1.65 ms/op  	|   3.98 ms/op	    |  300.73 ms/op	    |
|   gRPC add	    | 0.16 ms/op  	|   1.23	    |  170.95  	|
|   REST rawimg	    | 4.34 ms/op 	|   10.45 ms.op    |  1180.22 ms/op 	|
|   gRPC rawimg 	| 2.10 ms/op    |   9.04	    |  261.57 	|
|   REST dotproduct	| 2.60 ms/op  	|   5.49	    |   297.94 	|
|   gRPC dotproduct	| 0.16 ms/op  	|   1.21	    |  142.76  	|
|   REST jsonimg	| 20.00 ms/op  	|   55.01	    |  1353.42	 	|
|   gRPC jsonimg	| 7.47 ms/op    |   34.17	    |  210.85 	|
|   PING            |       |   0.41        |  144.34     |

## Write up:
gRPC was faster than REST in almost every test, especially when calls were small and frequent, like add. The main reason is connection reuse, the REST client opened a new TCP connection for each request, while gRPC kept one connection open and sent everything over it. For image tests, sending raw bytes, rawimg, was faster than sending base64 in JSON, jsonimage, this is because base64 makes the data roughly 33% bigger and adds extra encode and decode work. As soon as it went cross-region, the results mostly matched the ping time as the network distance dominated the cost, and both methods slowed down. Same-zone looked similar to localhost, which shows how fast Google’s internal network is. Overall gRPC is best for low-latency, high-throughput RPCs, while REST is fine but pays extra overhead per request, and even more if you send large JSON payloads.

