---
tags:
  - linux
  - networking
  - operating-systems
  - ssh
---
# How does SSH work

### [[SSH]] Version 2 Description

1. Connection initiated by client
2. Server responds with SSH version
3. Client switches to Binary Packet Protocol
4. Server will disclose its identity via its SSH key within `/etc/ssh`
5. If the client does not recognize this key, the user will be prompted
6. The client and server perform a diffie-hellman key exchange to generate the
   symmetric session key which will encrypt the rest of the session
7. The authentication stage begins

### SSH Version 1 Description

1. The connection is always initiated from the client to the server via a TCP
   connection to port 22. During this connection the client receives the protocol
   version supported by the server, and the ssh server package version. At this
   point, the client will continue if it supports version 2, otherwise it will break.
2. If the client decides to continue it will switch to a **Binary Packet Protocol**.
   This protocol contains a packet length of 32 bits (excluding the length field
   and message auth field), padding
3. The server will then disclose its identity to the client via an RSA public key
   on the server (usually in `/etc/ssh` or whatever).
4. If the client does not recognize this key then it will prompt the user with
   an unknown host warning and you'll have to type `yes` to proceed
5. The server then sends the client over its server key (not used in version 2).
   This key is regenerated every hour
6. The server will also send 8 random bytes (called checkbytes) to the client and
   expect these bytes within the client's reply
7. Finally, the server also sends back all the different forms of encryption it supports
8. The client created a random symmetric key using the list of algorithms it
   received from the server and then sends the symmetric key over to the server.
   This symmetric key will be used to encrypt and decrypt all communication during
   the SSH session. This symmetric key will be double-encrypted when it is sent
   over, using both the server host key, and the other server key (the one that
   regenerates every hour). Along with this double encrypted session key, the
   client will also send back the selected algorithm that it wants to use from
   the server's list
9. After the double-encrypted session key (the symmetric key above) has been sent
   to the server, the client will wait for the server to send a confirmation
   message encrypted with the session key. This proves to the client that the server
   has received the key, and is able to encrypt / decrypt with it.
10. After all of this, the authentication happens with one method listed below

### SSH Version 2 Differences

Very similar to version 1 minus a few advancements

1. Diffie-hellman key exchange is used rather than the hourly server key for sharing
   the session key
2. No rhosts support
3. SSH version 1 only allows negotiation to be done for the symmetric encryption
   algorithm other things (mac, compresstion, etc) are hard coded
4. Support for certificates is present
5. The server can force the client to use multiple authentication methods
6. The session key can change periodically via a rekey process

SSH Authentication

Password Authentication - A password (encrypted with the session key) is sent to
                          the server which is checked against the server's native
                          password authentication mechanisms
                          (/etc/passwd, ldap, etc)
Public Key Authentication - The client sends a request containing details about
                            the cryptography used for this public key auth. The
                            server will receive the request, generate a random
                            256 bit string as a challenge, and send the challenge
                            to the client. After receiving the challenge, the
                            client will decrypt it using its private key, and
                            send it back combined with the session key as an md5
                            hash. Once the server receives the hash it will
                            regenerate it to ensure it matches.

Public Key Authentication

1. The client begins by sending an ID for the key pair it would like to authenticate
   with to the server
2. The server checks the `authorized_keys` file for the user for the key ID
3. If a public key with a matching ID is found in the file, the server generates
   a random number and uses the public key to encrypt the number
4. The server sends the client the encrypted message
5. If the client actually has the associated private key, it will be able to decrypt
   the message using that key, revealing the original number
6. The client combines the decrypted number with the shared session key that is
   being used to encrypt the communication, and calculates the MD5 hash of this value
7. The client sends this MD5 hash back tot he server as an answer to the encrypted
   number message
8. The server uses the same shared session key and the original number that it
   sent to the client to calculate the MD5 value on its own. It compares its own
   value with the one the client sent back. If these two values match, it will
   prove that the client was in possession of the private key and the client is authenticated