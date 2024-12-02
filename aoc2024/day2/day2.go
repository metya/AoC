package main

import (
	"bufio"
	"flag"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func isSafe(level []int) bool {
	increasing := true
	decreasing := true
	for i := 1; i < len(level); i++ {
		diff := level[i] - level[i-1]
		if math.Abs((float64(diff))) < 1 || math.Abs(float64(diff)) > 3 {
			return false
		}
		if diff < 0 {
			decreasing = false
		}
		if diff > 0 {
			increasing = false
		}
	}
	return increasing || decreasing
}

func isSafeWithDeletion(level []int) bool {
	for i := 0; i < len(level); i++ {
		modified := append([]int{}, level[:i]...)
		modified = append(modified, level[i+1:]...)
		if isSafe(modified) {
			return true
		}
	}
	return false
}

func main() {
	args := flag.Bool("example", false, "example or input, just type the 'example' for example")
	// Read input from file
	flag.Parse()
	filename := "input.txt"
	if *args {
		filename = "example.txt"
	}
	file, err := os.Open(filename)
	if err != nil {
		panic("Can't read the file")
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	safeCount := 0
	safeCountWithDeletion := 0
	for {
		line, _, err := reader.ReadLine()
		if len(line) == 0 {
			break
		}
		if err != nil {
			fmt.Println(err)
		}
		var level []int
		for _, num := range strings.Fields(string(line)) {
			numi, _ := strconv.Atoi(num)
			level = append(level, numi)
		}
		if isSafe(level) {
			safeCount++
		} else {
			if isSafeWithDeletion(level) {
				safeCountWithDeletion++
			}
		}

	}

	fmt.Println("Part 1 Safe Counts:", safeCount)
	fmt.Println("Part 2 Safe Counts With Deletion:", safeCount+safeCountWithDeletion)
}
