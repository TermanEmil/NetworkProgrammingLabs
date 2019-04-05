# HTTP protocol

## Objectives:
  - Understand the HTTP protocol and the basic methods
  - GET, POST, DELETE, PUT, PATCH, HEAD
  - Semnification of status codes
  - Types of HTTP conections
  - Basic concepts of HTTP method : headers, servers, clients, methods

## Tasks:
 Implement an HTTP client that should use the HTTP methods for performing the requests.

### Get
~~~shell
curl -X GET "http://httpbin.org/ip" -H "accept: application/json"
~~~

**Result:** (the requester's IP)

~~~json
{
  "origin": "81.180.74.158, 81.180.74.158"
}
~~~

### Post
~~~sh
curl -X POST "http://httpbin.org/post"
~~~

**Result:**

~~~json
{
  "args": {},
  "data": "",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Content-Length": "0",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.54.0"
  },
  "json": null,
  "origin": "81.180.74.158, 81.180.74.158",
  "url": "https://httpbin.org/post"
}
~~~

### Head
~~~sh
curl -I "http://httpbin.org/headers"
~~~

**Result:**

~~~
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: *
Content-Length: 105
Content-Type: application/json
Date: Fri, 05 Apr 2019 10:49:29 GMT
Server: nginx
Connection: keep-alive
~~~

### Put
~~~sh
curl -X PUT "http://httpbin.org/put"
~~~

### Delete
~~~sh
curl -X DELETE "http://httpbin.org/delete"
~~~


## Conclusion
**POST vs PUT vs DELETE**

 * PUT & DELETE - idempotent
 * PUT - updates/replaces a resource
 * POST - creates a new resource with some side effects
 * PUT & DELETE: If the network is botched and the client is not sure whether his request made it through, it can just send it a second (or 100th) time, and it is guaranteed by the HTTP spec that this has exactly the same effect as sending once
