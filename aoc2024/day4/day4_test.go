package main

import "testing"

func BenchmarkF(b *testing.B) {
	for i := 0; i < b.N; i++ {
		main()
	}
}
