# Testing

Golang has pretty good built in support for unit testing within the `testing` package in the stdlib, although for easier assertions
it's worth installing [testify](github.com/stretchr/testify).

## Examples

Let's say we have a simple calculator package which does some math...
```go
package calculator

func Add(a int, b int) int {
    return a + b
}
```

In it's simplest form, a unit test would look something like this...
```go
package calculator_test

import (
    "testing"

    "github.com/stretchr/testify/assert"

    "github.com/crgwilson/go-example/calculator"
)

func TestAdd(t *testing.T) {
    expected := 2
    got := calculator.Add(1, 1)
    assert.Equal(t, got, expected)
}
```

But mostly, you'll probably want to parametrize your tests...
```go
package calculator_test

import (
    "testing"

    "github.com/stretchr/testify/assert"

    "github.com/crgwilson/go-example/calculator"
)

func TestAdd(t *testing.T) {
    cases := []struct {
        Name        string
        FirstInput  int
        SecondInput int
        Expected    int
    }{
        {
            "1+1",
            1,
            1,
            2,
        },
        {
            "2+2",
            2,
            2,
            4,
        }
    }
    for _, test := range cases {
        t.Run(test.Name, func(t *testing.T) {
            assert.Equals(t, calculator.Add(test.FirstInput, test.SecondInput), test.Expected)
        }
    }
}
```

This is good for a simple test, but what about if we want to unit test an HTTP server? Well there is `net/http/httptest` which can help! Here is how
to create a rather simple HTTP server and test it with a real HTTP request.
```go
package handlers_test

import (
    "io"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/stretchr/testify/assert"
)

func TestMyHandler(t *testing.T) {
    // Create a handler which we can test
    dummyHandler := func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Oh Snap!"))
    }

    // Create a test http server with our new handler
    mux := http.NewServeMux()
    mux.HandleFunc("GET /test", dummyHandler)
    server := httptest.NewServer(mux)
    defer server.Close()

    // Now test it with a request recorder
    resp, err := http.Get(server.URL + "/test")
    assert.NoError(t, err)
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    assert.Equal(t, resp.StatusCode, http.StatusOK)
    assert.Equal(t, body, []byte("Oh Snap!"))
}
```

Or a more practical example, let's say you want to stub out an external dependency to unit test an API client...
```go
package client_test

import (
    "fmt"
    "io"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/stretchr/testify/assert"

    "github.com/crgwilson/go-example/client"
)

func TestMyCoolAPIClient(t *testing.T) {
    testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        expectedPath := "/foo"
        assert.Equal(t, r.Method, http.MethodPost, fmt.Sprintf("Expected POST, but got %s", r.Method))
        assert.Equal(t, r.URL.Path, expectedPath, fmt.Sprintf("Expected request to path %s, but got", expectedPath, r.URL.Path))
        w.Write([]byte("It worked!"))
    }))
    defer testServer.Close()

    testClient := client.New()
    err := testClient.CreateFoo()
    assert.NoError(t, err)
}
```
