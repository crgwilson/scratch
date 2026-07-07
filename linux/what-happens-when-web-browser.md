# What happens when you type google.com into your web browser

## 1. The "g" key is pressed

The "g" key is pressed and the browser receives an event which triggers auto-complete
functionality to kick in. This will search your bookmarks, popular search terms,
etc.

## 2. The enter key bottoms out

The enter key reaches the bottom of tis range and an electrical circuit specific
to the enter key is closed (either directly or capacitively). This allows a small
amount of current to flow into the logical circuitry of the keyboard, which scans
the state of each key switch, debounces the electrical noise of the rapid intermittent
closure of the switch, and converts it into a keycode integer, in this case 13.
The keyboard controller then encodes the keycode for transport to the computer.
This is now almost universally over a USB or bluetooth connection, but historically
PS/2 or ADB were also used.

The message travels over to the computer, which receives it and throws an interrupt.
The desktop environment will use an event driver to acquire the keypress and redirect
it into the focused window. Once received, the character is written out to the window.

## 3. Parse URL

The browser takes the URL and parses it to obtain...

* The protocol `http` / `https`
* The resource `/` (since its just google.com)

## 4. URL or search term

If there is no valid protocol or domain name that could be obtained from the
entered text the browser will assume it is a search term and forward it to the
default web search engine. In many cases the URL has a special piece of text appended
to it to tell the search engine that it came from a particular browser's URL bar.

## 5. Convert non-ASCII unicode characters in hostname

* The browser checks the hostname for characters that are not `a-z`, `A-Z`, `0-9`,
  `-`, or `.`
* Since the hostname is `google.com` there won't be any, but if there was the
  browser would apply a "Punycode" encoding to the hostname portion of the URL

## 6. Check HSTS list

* The browser checks its "proloaded HSTS (HTTP Strict Transport Security)" list.
  This is a list of websites that have requested to be contacted via HTTPS only.
* If the website is in that list, then the browser will send its request via
  HTTPS instead of HTTP. Otherwise, the initial request will be sent via HTTP.

## 7. DNS lookup

* The browser will check if the domain is in its cache
* If not, the browser will call `gethostbyname` library function (may vary depending
  on OS) to do the lookup
* `gethostbyname` checks if the hostname can be resolved by reference in the local
  `hosts` file, before trying to resolve via DNS
* If its not in the host file then it will send a request to the configured DNS
  server from the network stack
* If the DNS server is on the same subnet the network library follows the ARP
  process below for the DNS server
* If the DNS server is on a different subnet then the library will follow the
  ARP process below to reach the default gateway

## 8. ARP process

In order to send an ARP (Address Resolution Protocol) broadcast the network stack
library needs the target IP address to look up. It also needs to know the MAC address
of the interface it will use to send out the ARP broadcast.

The ARP cache is first checked for an ARP entry for out target IP. If it is in
the cache, the library function returns the result: `Target IP = MAC`

If the entry is not in the ARP cache:

* The route table is looked up, to see if the Target IP address is on any of the
  subnets on the local route table. If it is, the library uses the interface
  associated with that subnet. If it is not, the library uses the interface that
  has the subnet of our default gateway.
* The MAC address of the selected network interface is looked up
* The network library sends a Layer 2 (data link of the OSI model) ARP request

`ARP Request:`

```
Sender MAC: interface:mac:address:here
Sender IP: interface.ip.goes.here
Target MAC: FF:FF:FF:FF:FF:FF (Broadcast)
Target IP: target.ip.goes.here
```

Depending on the type of hardware is between the computer and the router:

Directly connected:

* If the computer is directly connected to the router then the router response
  with an `ARP Reply`

Hub:

* If the computer is connected to a hub then the hub will broadcast the ARP
  request out all other ports. If the router is connected on the same wire, it
  will response with an `ARP reply`

Switch:

* If the computer is connected to a switch then the switch will check its local
  CAM/MAC table to see which port has the MAC address we're looking for. If the
  switch has no entry for the MAC address it will rebroadcast the ARP request out
  all ports.
* If the switch has an entry in its table then it will send the ARP request to
  the port that has the MAC address we're looking for
* If the router is on the same wire, it will respond with an `ARP Reply`

## 9. Arp reply

`ARP Reply:`

```
Sender MAC: target:mac:address:here
Sender IP: target.ip.goes.here
Target MAC: interface:mac:address:here
Target IP: interface.ip.goes.here
```

Now that the network library has the IP address of either our DNS server or the
default gateway it can resume its DNS process:

* The DNS client establishes to a socket to UDP port 53 on the DNS server, using
  a port above 1023
* If the reponse size is too large, TCP will be used instead
* If the local/ISP DNS server does not have it, then a recursive search is
  requested and that flows up the list of DNS servers until the SOA is reached,
  and if an answer is found it is returned.

## 10. Opening a socket

Once the browser receives the IP address of the destination server, it takes that
and the given port number from the URL (the HTTP protocol defaults to 80, and
HTTPS is 443), and makes a call to the system library function named `socket`
and requests a TCP socket stream - `AF_INET/AF_INT6` and `SOCK_STREAM`

* This request is first passed to the transport layer where a TCP segment is created.
  The destination port is added to the header, and the source port is chosen from
  within the kernel's dynamic port range (ip_local_port_range in Linux)
* This segment is sent to the Network Layer, which wraps an additional IP header.
  The IP address of the destination server as well as that of the current machine
  is inserted to form a packet
* The packet next arrives at the Link layer. A frame header is added that includes
  the MAC address of the machine's NIC as well as the MAC address of the gateway
  (local rotuer). As before, if the kernel does not know the mac address of the
  gateway, it must broadcast an ARP query to find it.

At this point the packet is ready to be transmitted through either:

* Ethernet
* WiFi
* Cellular data network

Eventually, the packet will reach the router managing the local subnet. From there,
it will continue to travel to the autonomous system's (AS) border routers, other
ASes, and finally to the destination server. Each router along the way extracts
the destination address from the IP header and routes it to the appropriate next
hop. The time to live (TTL) field in the IP header is decremented by one for each
router that passes. The packet will be dropped if the TTL field reaches 0 or if
the current router has no space in tis queue.

This send and receive happens multiple times following the TCP connection flow:

* Client chooses an initial sequence number (ISN) and sends the packet to the server
  with the SYN bit set to indicate it is setting the ISN
* The server receives the SYN and...
    1. Chooses its own initial sequence number
    2. Sets SYN to indicate it is choosing its ISN
    3. Copies the client ISN + 1 to its ACK field and adds the ACK flag to indicate
       its acknowledging receipt of the first packet
* Client acknowledges the connection by sending a packet
    1. Increase its own sequence number
    2. Increases the receiver acknowledgment number
    3. Sets ACK field
* Data is transferred as follows:
    1. As one side sends N bytes, it increases its SEQ by that number
    2. When the other side acknowledges receipt of that packet (or string of packets),
       it sends an ACK packet with the ACK value equal to the last received sequence
       from the other
* To close the connection:
    1. The closes sends a FIN
    2. The other side ACKs the FIN and sends its own FIN
    3. The closer acknowledges the other side's FIN with an ACK

## 11. TLS handshake

* The client computer sends a `ClientHello` message to the server with its Transport
  Layer Security (TLS) version, list of cipher algorithms and compression methods
  available
* The server replies with a `ServerHello` message to the client with the TLS version,
  selected cipher, selected compression methods and the server's public certificate
  signed by a CA. The certificate cotnains a public key that will be used by the
  client to encrypt the rest of the handshake until a symmetric key can be agreed
  upon
* The client verifies the server digital certificate against a list of trusted
  CAs. If trust can be established based ont he CA, the client generates a string
  of pseudo-random bytes and encrypts this with the server's public key. These
  random bytes can be used to determine the symmetric key
* The server decrypts the random bytes using its private key and uses these bytes
  to generate its own copy of the symmetric master key
* The client sends a `Finished` message to the server, encrypting a hash of the
  transmission up to this point with the symmetric key
* The server generates its own has, and thend ecrypts the client-sent hash to
  verify that it matches. If it does, it sends its own `Finished` message to the
  client, also encrypted with the symmetric key
* From now on the TLS session transmits the application (HTTP) data encrypted
  with the agreed symmetric key

## 12. If a packet is dropped

Sometimes, due to network congestion or flaky hardware connections, TLS packets
will be dropped before they get to their destination. The sender then has to decide
how to react. The algorithm for this is called TCP congestion control.
This varies depending on the server, but the most common algorithms are cubic on
newer operating systems and New Reno on almost all others

* Client chooses a congestion window based on the maximum segment size (MSS) of
  the connection
* For each packet acknowledged, the window doubles in size until it reaches the
  "slow-start threshold". In some implementations, this threshold is adaptive
* After reaching the slow start threshold, the window increases additively for
  each packet acknowledged. If a packet is dropped, the window reduces exponentially
  until another packet is acknowledged

## 13. HTTP protocol

If the web browser used was written by Google, instead of sending an HTTP request
to retrieve the page, it will send a request to try and negotiate with the server
an "upgrade" from HTTP to the SPDY protocol

If the client is using the HTTP protocol and does not support SPDY, it sends a
request to the server of the form:

```
GET / HTTP/1.1
Host: google.com
Connection: close
[other headers]
```

Where `[other headers]` refers to a series of colon-separated key/value pairs
formatted as per the HTTP spec and separated by single new lines. This also
assumes the web browser is using `HTTP/1.1`, otherwise it may not include the
`Host` header in the request and the version specified in the `GET` request will
either by `HTTP/1.0` or `HTTP/0.9`

HTTP/1.1 defines the "close" connection option for the sender to signal that the
connection will be closed after completion of the response. For example,

"Connection: close"

HTTP/1.1 applications that do not support persistent connections MUST include the
"close" connection option in every message

After sending the request and ehaders, the web browser sends a single blank newline
to the server indicating that the content of the request is done.

The server responds with a response code denoting the status of the request and
responds with a response of the form:

```
200 OK
[response headers]
```

Followed by a single newline, and then sends a payload of the HTML content of
`www.google.com`. The server may then either close the connection, or if headers
sent by the client requested it, keep the connection open to be reused for future
requests

If the HTTP headers sent by the web browser included sufficient information for
the web server to determine if the version of the file cached by the web browser
has been unmodified since the last retrieval (ie - if the web browser included an
`ETag` header), it may instead respond with a request of the form:

```
304 Not Modified
[response headers
```

And no payload, and the web browser instead retrieves the HTML from its cache.

After parsing the HTML, the web browser (and server) repeats this process for every
resource (image, CSS, favicon.ico, etc) referenced by the HTML page, except
instead of `GET / HTTP/1.1` the request will be `GET /$(URL relative to www.google.com)
HTTP/1.1`

If the HTML referenced a resource on a different domain then `www.google.com`,
the web browser goes back to the steps involved in resolving the other domain,
and follows all steps up to this point for that domain. The `Host` header in the
request will be set to the appropriate server name instead of `google.com`.

## 14. HTTP Server Request Handle

The HTTPD (HTTP Daemon) server is the one handling the requests/responses on the
server side. The most common HTTPD servers are Apache and NGINX for linux and
IIS for windows.

* The HTTPD receives the request
* The server breaks down the request to the following parameters:
    1. HTTP request method
    2. Domain, in this case `google.com`
    3. Requested path/page, in this case /
* The server verifies that there is a Virtual Host configured on the server that
  corresponds with google.com
* The server verifies that google.com can accept GET requests
* The server verifies taht the client is allowed to use this method (by IP,
  authentication, etc)
* If the server has a rewrite module installed (like mod_rewrite for Apache or
  URL rewrite for IIS), it tries to match the request against one of the configured
  rules. If a matching rule is found, the server uses that rule to rewrite the request.
* The server goes to pull the content that corresponds with the request, in our
  case it will fall back to the index file as "/" is the main file
* The server parses the file accoding to the handler. If google is running on
  PHP, the server uses PHP to interpret the index file, and streams the output
  back to the client.

## 15. Behind the scenes of the Browser

Once the server supplies the resources (HTML, CSS, JS, images, etc) to the browser
it undergoes the below process:

* Parsing - HTML, CSS, JS
* Rendering - Construct DOM tree -> Render tree -> Layout of render tree ->
  painting the render tree

## 16. Browser

The browser's functionality is to present the web resource you choose, by requesting
it from the server and displaying it in a browser window. The resource is usually
an HTML document, but may also be a PDF, image, or some other type of content.
The location of the resource is specified by the user using a URI
(Uniform Resource identifier).

The way the browser interprets and displays HTML files is specified in the HTML
and CSS spec. There specs are maintained by the W3C (World Wide Web Consortium)
organization, which is the standards organization for the web.

Browser user interfaces have a lot in common with each other. Among the common user
interface elements are:

* An address bar for inserting a URI
* Back and forward buttons
* Bookmarking options
* Refresh and stop buttons for refreshing or stopping the loading of current documetns
* Home button that takes you to your home page

## 17. Browser High Level Structure

The components of the browsers are:

* User interface: The user interface includes the address bar, back/forward button,
  bookmarking menu, etc/ Every part of the browser display expect the window
  where you see the requested page.
* Browser engine: The browser engine marshals actions between the UI and the
  rendering engine
* Rendering engine: The rendering engine is responsible for displaying requested
  content. For example if the requested content is HTML, the rendering engine parses
  HTML and CSS, and displays the parsed content on the screen
* Networking: The networking handles network calls such as HTTP requests, using
  different implementations for different platforms behind a platform-independent
  interface
* UI backend: The UI backend is used for drawing basic widgets like combo boxes
  and windows. This backend exposes a generic interface that is not platform
  specific. Underneath it uses operating system user interface methods.
* Javascript engine: The javascript engine is used to parse and execute
  Javascript code.
* Data storage: The data storage is a persistence layer. The browser may need to
  save all sorts of data locally, such as cookies. Browsers also support storage
  mechanisms such as localStorage, IndexedDB, WebSQL, and FileSystem

## 18. HTML Parsing

The rendering engine starts getting the contents of the requested document from
the networking layer. This will usually be done in 8kb chunks.

The primary job of HTML parser is to parse the HTML markup into a parse tree.

The output tree (the "parse tree") is a tree of DOM element and attribute nodes.
DOM is short for Document Object Model. It is the object presentation of the HTML
document and the interface of HTML elements to the outside world like
Javascript. The root of the tree is the "Document" object. Prior of any
manipulation via scripting, the DOM has an almost one-to-one relation to the markup.

The parsing algorithm

HTML cannot be parsed using the regular top-down or bottom-up parsers.

The reasons are:

* The forgiving nature of the language
* The fact that browsers have traditional error tolerance to support well known
  cases of invalid HTML
* The parsing process is reentrant. For other languages, the source doesn't
  change during parsing, but in HTML, dynamic code (such as script elements
  containing document.write() calls) can add extra tokens, so the parsing process
  actually modifies the input.

Unable to use the regular parsing techniques, the browser utilizes a custom parser
for parsing HTML. The parsing algorithm is described in detail by the HTML5 spec.

The algorithm consists of two stages: tokenization and tree construction.

Actions when the parsing is finished

The browser begins fetching external resources linked to the page (CSS, images,
JS files, etc).

At this stage the browser marks the document as interactive and starts parsing
scripts that are in "deferred" mode: those that should be executed after the
document is parsed. The document state is set to "complete" and a "load" event
is fired.

Note there is never an "Invalid syntax" error on an HTML page. Browsers fix any
invalid content and go on.

## 19. CSS interpretation

* Parse CSS files, `<style>` tag contents, and `style` attribute values using
  "CSS lexical and syntax grammar"
* Each CSS file is parsed into a `StyleSheet object`, where each object contains
  CSS rules with selectors and objects corresponding CSS grammar
* A CSS parser can be top-down or bottom-up when a specific parser generator is used

## 20. Page rendering

* Create a "Frame Tree" or "Render Tree" by traversing the DOM nodes, and
  calculating the CSS style values for each node
* Calculate the preferred width of each node in the "Frame Tree" bottom up by
  summing the preferred width of the child nodes and the node's horizontal margins,
  borders, and padding
* Calculate the actual width of each node top-down by allocating each node's
  available width to its children
* Calculate the height of each node bottom-up by applying text wrapping and summing
  the child node heights and the node's margins, borders, and padding
* Calculate the coordinates of each node using the information calculated above
* More complicated steps are taken when elements are `floated`, positioned `absolutely`
  or `relatively`, or other complex features are used. See
  `http://dev.w3.org/csswg/css2/` and
  `http://www.w3.org/Style/CSS/current-work` for more details
* Create layers to describe which parts of the page can be animated as a group
  without being re-rasterized. Each frame / render object is assigned to a layer
* Textures are allocated to each layer of the page
* The frame / render objects for each layer are traversed and drawing commands
  are executed for their respective layer. This may be rasterized by the CPU or
  drawn on the GPU directly using D2D/SkiaGL
* All of the above steps may reuse calculated values from the last time the webpage
  was rendered, so that incremental changes require less work
* The page layers are sent to the compositing process where they are combined with
  layers for other visibile content like the browser chrome, iframes and addon panels
* Final layer positions are computed and the composite commands are issued via
  Direct3D/OpenGL. The GPU command buffer(s) are flushed to the GPU for asynchronous
  rendering and the frame is sent to the window server

## 21. GPU Rendering

* During the rendering process the graphical computing layers can use general
  purpose `CPU` or the graphical processor `GPU` as well
* When using `GPU` for graphical rendering computations the graphical software
  layers split the task into multiple pieces, so it can take advantage of `GPU`
  massive parallelism for the float point calculations required for the rendering
  process.

## 22. Window Server

Post-rendering and user-induced execution

After rendering has completed, the browser executes Javascript code as a result
of some timing mechanism (such as a Google Doodle animation) or user interaction
(typing a query into the search box and receiving suggestions). Plugins such as
Flash or Java may execute as well, although not at this time on the Google homepage.
Scritps can cause additional network requests to be performed, as well as modify
the page or its layout, causing another round of page rendering and painting.