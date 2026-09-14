# TCP-Chat

A simple client-server chat application written in Python using raw TCP sockets.

The project was created to learn how TCP connections work at the application level and how a custom communication protocol can be built on top of a TCP connection.

## Features

* Client-server architecture
* Communication over TCP sockets
* Custom application-level protocol
* Text message exchange
* IP-based identification
* Configurable server host and port
* Connection timeout handling
* No external networking framework required

## Architecture

The application consists of two main components:

```text
┌──────────────┐
│    Client    │
└──────┬───────┘
       │
       │ TCP
       │
       ▼
┌──────────────┐
│    Server    │
└──────────────┘
```

The client establishes a TCP connection to the server and exchanges data using the project's custom protocol.

The server receives client requests, processes them, and sends responses back to the connected client.

## Custom Protocol

The project uses a simple text-based protocol. Messages are separated using:

```text
\r\n\r\n
```

The main commands are:

```text
START <username>

CONTENT

POST <message>

STOP
```

### Starting a connection

The client first identifies itself with:

```text
START <username>
```

### Sending a message

A message can be sent using:

```text
POST <message>
```

### Receiving messages

The server can return accumulated chat content using:

```text
CONTENT
```

### Closing the connection

The client can terminate the session with:

```text
STOP
```

The delimiter `\r\n\r\n` is used to determine where one protocol message ends.

## Why TCP?

TCP provides a reliable, ordered byte stream between the client and server.

An important part of this project is understanding that TCP does **not** preserve application-level messages.

For example, one call to:

```python
socket.recv()
```

does not necessarily correspond to one message.

A message may arrive in multiple parts:

```text
recv() → "POST Hel"
recv() → "lo\r\n\r\n"
```

or multiple protocol messages may arrive together:

```text
recv() → "POST Hello\r\n\r\nPOST World\r\n\r\n"
```

The application therefore needs its own message framing mechanism. This project uses `\r\n\r\n` as a delimiter.

## Requirements

* Python 3
* A local network connection if the client and server run on different machines

No external Python packages are required.

## Running the Server

Start the server with:

```bash
python3 server.py
```

The server waits for incoming TCP connections.

## Running the Client

In another terminal:

```bash
python3 client.py
```

Enter the server address and connect to the running server.

For local testing, the server can be accessed through:

```text
127.0.0.1
```

## Running on a Local Network

To test the application between two computers:

1. Start the server on one machine.
2. Determine the server's local IP address.
3. Start the client on another machine.
4. Connect the client to the server's IP address and port.

Example:

```text
Server: 192.168.1.100
Client: 192.168.1.101

Client ───── TCP ─────> Server
```

Both machines must be able to reach the selected TCP port.

## Project Structure

```text
TCP-Chat/
├── client.py       # Client implementation
├── server.py       # Server implementation
├── LICENSE         # MIT License
└── README.md       # Project documentation
```

## What I Learned

This project was developed as a practical exercise in computer networking and Python.

The main topics explored were:

* TCP sockets
* Client-server architecture
* TCP byte streams
* Application-layer protocols
* Message framing
* Socket timeouts
* Connection handling
* Basic protocol parsing
* Network communication between machines

## Limitations

This is a learning project and is **not intended for production use**.

Current limitations include:

* Limited concurrent-client handling
* Basic protocol validation
* No encryption
* No persistent database
* No authentication system
* Limited error handling
* Limited protection against malformed or excessively large input

These limitations are intentional areas for future development.

## Future Development

Possible improvements include:

* [ ] Support multiple clients concurrently
* [ ] Improve protocol parsing and validation
* [ ] Add message size limits
* [ ] Improve connection and error handling
* [ ] Add persistent message storage
* [ ] Add user authentication
* [ ] Add private messages
* [ ] Add chat rooms
* [ ] Add logging
* [ ] Add automated tests
* [ ] Add encrypted communication
* [ ] Improve documentation

## License

This project is licensed under the MIT License.

See [`LICENSE`](LICENSE) for the full license text.
