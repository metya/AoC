package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	args := flag.Bool("example", false, "example or input")
	flag.Parse()
	filename := "input.txt"
	if *args {
		filename = "example.txt"
	}
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var equations []Equation
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		equations = append(equations, parseEquation(line))
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return
	}

	// part 1
	start := time.Now()
	totalSum := 0
	for _, eq := range equations {
		if checkOperators(eq.numbers, eq.testValue, 0, eq.numbers[0], false) {
			totalSum += eq.testValue
		}
	}
	end1 := time.Since(start)

	// part2
	start = time.Now()
	totalSumWithMerged := 0
	for _, eq := range equations {
		if checkOperators(eq.numbers, eq.testValue, 0, eq.numbers[0], true) {
			totalSumWithMerged += eq.testValue
		}
	}
	end2 := time.Since(start)

	fmt.Println("Total Sum:", totalSum, "with time:", end1)
	fmt.Println("Total Sum With Merged:", totalSumWithMerged, "with time:", end2)
}

type Equation struct {
	testValue int
	numbers   []int
}

func parseEquation(line string) Equation {
	parts := strings.Split(line, ":")
	testValue, _ := strconv.Atoi(strings.TrimSpace(parts[0]))
	numberStrings := strings.Fields(parts[1])
	var numbers []int
	for _, num := range numberStrings {
		n, _ := strconv.Atoi(num)
		numbers = append(numbers, n)
	}
	return Equation{testValue: testValue, numbers: numbers}
}

func checkOperators(numbers []int, target int, index int, currentValue int, merge bool) bool {
	if index == len(numbers)-1 {
		return currentValue == target
	}

	nextNumber := numbers[index+1]

	// +
	if checkOperators(numbers, target, index+1, currentValue+nextNumber, merge) {
		return true
	}

	//  *
	if checkOperators(numbers, target, index+1, currentValue*nextNumber, merge) {
		return true
	}

	// ||
	if merge {
		merged, _ := strconv.Atoi(fmt.Sprintf("%v%v", currentValue, nextNumber))
		if checkOperators(numbers, target, index+1, merged, merge) {
			return true
		}
	}

	return false
}
