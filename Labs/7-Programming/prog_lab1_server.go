// go run ctf_server.go
package main

import (
	"fmt"
	"net"
	"strconv"
)

// Modify this variable for the flag string
var flag = "FLAG{ASCII_NUMBERS}"

func main() {
	// Listen on port 43239
	listener, err := net.Listen("tcp", ":43239")
	if err != nil {
		fmt.Println("Error starting server:", err)
		return
	}
	defer listener.Close()
	fmt.Println("Server listening on port 43239...")

	for {
		// Accept connection
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting connection:", err)
			continue
		}

		// Handle client connection in a goroutine
		go handleClient(conn)
	}
}

func handleClient(conn net.Conn) {
	defer conn.Close()

	// Convert the flag string to ASCII values
	asciiValues := convertToASCII(flag)

	// Send the ASCII values to the client, one per line
	for _, val := range asciiValues {
		conn.Write([]byte(strconv.Itoa(val) + "\n"))
	}
}

// convertToASCII converts a string to a slice of ASCII values
func convertToASCII(s string) []int {
	var ascii []int
	for _, c := range s {
		ascii = append(ascii, int(c))
	}
	return ascii
}
