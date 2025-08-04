# Network Programming

## Endianness

Endianness describes the ordering of a set of bits. Big Endian places the most significant bit on the left, whereas Little Endian is the inverse.
[RFC 1700](https://www.rfc-editor.org/rfc/rfc1700) defines the order for protocols within the Internet Protocol suite to be big endian.

## Bitwise Operations

Bitwise operations allow you to interact with individual bits from a bit / byte array, binary numeral, or a bit string. They are commonly used in network programming for encoding and decoding structs into packets to be sent over the wire.

**AND:**
```
    0101 (decimal 5)
AND 0011 (decimal 3)
  = 0001 (decimal 1)
```

**OR:**
```
   0101 (decimal 5)
OR 0011 (decimal 3)
 = 0111 (decimal 7)
```

**XOR:**
```
    0101 (decimal 5)
XOR 0011 (decimal 3)
  = 0110 (decimal 6)
```

**Bit shifts:**
Bit shifting is sometimes considered a bitwise operation. In short, the bits are moved, _or shifted_ to the left or right. Bit shifts can be logical (0s replace the bits which were shifted out), or circularly (bits shifted out move to the other side of the byte).

```
t := uint8(1)        // 00000001
fmt.Println(t << 1)  // 00000010
fmt.Println(t >> 1)  // 00000000
fmt.Println(t << 7)  // 10000000
fmt.Println(t << 8)  // 00000000
```

### Cheatsheet

**Operators:**

| Operation | Result | Description |
|---------- | ------ | ----------- |
| `0011 & 0101` | `0001` | Bitwise AND |
| `0011 \| 0101` | `0111` | Bitwise OR |
| `0011 ^ 0101` | `0110` | Bitwise XOR |
| `^0101` | `1010` | Bitwise NOT |
| `0011 &^ 0101` | `0010` | Bitclear (AND NOT) |
| `00110101<<2` | `11010100` | Left shift |
| `00110101<<100` | `00000000` | No upper limit on shift count |
| `00110101>>2` | `00001101` | Right shift |
_Examples shown are built-in Golang operators. Other languages are similar._

**Tips & Tricks:**

| Operation | Example |
| --------- | ------- |
| Convert letter to lowercase by ORing by space | `(x \| " ")` |
| Convert letter to uppercase by ANDing by underscore | `(x & "_")` |
| Invert a letter's case by XORing by space | `(x ^ " ")` |
| Get letter's position in the alphabet by ANDING by `chr(31)/binary("11111")/hex("1F")` | `(x & (chr(31)/binary("11111")/hex("1F")))` |
_For more, see [Bit Twiddling Hacks](http://graphics.stanford.edu/~seander/bithacks.html)_
