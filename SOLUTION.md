
|  Method 	        | Local | Same-Zone |  Different Region 	|
|---	            |---	|---	    |---	                |---	|
|   REST add        | 1.65 ms/op  	|   3.98 ms/op	    |  300.73 ms/op	    |
|   gRPC add	    | 0.16 ms/op  	|   	    |    	|
|   REST rawimg	    | 4.34 ms/op 	|   10.45 ms.op    |  1180.22 ms/op 	|
|   gRPC rawimg 	| 2.10 ms/op    |   	    |   	|
|   REST dotproduct	| 2.60 ms/op  	|   5.49	    |   297.94 	|
|   gRPC dotproduct	| 0.16 ms/op  	|   	    |    	|
|   REST jsonimg	| 20.00 ms/op  	|   55.01	    |  1353.42	 	|
|   gRPC jsonimg	| 7.47 ms/op    |   	    |   	|
|   PING            |       |           |       |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.