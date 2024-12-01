package main

import (
	"testing"
)

func BenchmarkExample(b *testing.B) {
	for i := 0; i < b.N; i++ {
		readInput("example.txt", false)
	}
}

func BenchmarkInput(b *testing.B) {
	for i := 0; i < b.N; i++ {
		readInput("input.txt", false)
	}
}
