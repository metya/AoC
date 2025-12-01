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
	example := flag.Bool("example", false, "example or input")
	flag.Parse()
	filename := "input.txt"
	if *example {
		filename = "example.txt"
	}
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Ошибка при открытии файла:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	line := scanner.Text()
	stones := parseInput(line)

	// part 1
	start := time.Now()
	steps := 25
	result := simulateBlinks(stones, steps)
	end1 := time.Since(start)

	fmt.Println("Total count of stones after", steps, "steps:", len(result), "in time:", end1)
}

func parseInput(input string) []int {
	parts := strings.Fields(input)
	stones := make([]int, len(parts))
	for i, part := range parts {
		stones[i], _ = strconv.Atoi(part)
	}
	return stones
}

func simulateBlinks(stones []int, steps int) []int {
	for step := 0; step < steps; step++ {
		var newStones []int
		for _, stone := range stones {
			if stone == 0 {
				newStones = append(newStones, 1)
			} else if len(strconv.Itoa(stone))%2 == 0 {
				left, right := splitStone(stone)
				newStones = append(newStones, left, right)
			} else {
				newStones = append(newStones, stone*2024)
			}
		}
		stones = newStones
	}
	return stones
}

func splitStone(stone int) (int, int) {
	str := strconv.Itoa(stone)
	mid := len(str) / 2
	left, _ := strconv.Atoi(str[:mid])
	right, _ := strconv.Atoi(str[mid:])
	return left, right
}
