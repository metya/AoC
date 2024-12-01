package main

import (
	"bufio"
	"flag"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func readInput(filename string, v bool) ([]int, []int, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, nil, err
	}
	defer file.Close()

	var leftList, rightList []int
	reader := bufio.NewReader(file)

	for {
		line, _, err := reader.ReadLine()
		if len(line) == 0 {
			break
		}
		numbers := strings.Fields(string(line))
		if v {
			fmt.Println(numbers)
		}
		if len(numbers) != 2 {
			return nil, nil, fmt.Errorf("invalid line format: %s", line)
		}

		// Convert the numbers to integers
		leftNum, err := strconv.Atoi(numbers[0])
		if err != nil {
			return nil, nil, err
		}
		rightNum, err := strconv.Atoi(numbers[1])
		if err != nil {
			return nil, nil, err
		}

		leftList = append(leftList, leftNum)
		rightList = append(rightList, rightNum)
	}

	return leftList, rightList, nil
}

func totalDistance(leftList, rightList []int) int {
	sort.Ints(leftList)
	sort.Ints(rightList)

	total := 0
	for i := 0; i < len(leftList); i++ {
		total += int(math.Abs(float64(leftList[i] - rightList[i])))
	}

	return total
}

func similarityScore(leftList, rightList []int) int {
	rightFrequency := make(map[int]int)
	for _, num := range rightList {
		rightFrequency[num]++
	}

	total := 0
	for _, num := range leftList {
		total += num * rightFrequency[num]
	}

	return total
}

func main() {
	args := flag.String("filename", "input", "example or input, just type the filename")
	// Read input from file
	flag.Parse()

	filename := fmt.Sprint(*args + ".txt")
	leftList, rightList, err := readInput(filename, true)
	if err != nil {
		fmt.Println("Error reading input:", err)
		return
	}

	// Calculate and print the result
	result1 := totalDistance(leftList, rightList)
	result2 := similarityScore(leftList, rightList)
	fmt.Println("Part 1 Total Distance:", result1)
	fmt.Println("Part 2 Total Similarity:", result2)
}
