package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
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
	var rules []string
	var updates [][]int
	readingRules := true

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			readingRules = false
			continue
		}
		if readingRules {
			rules = append(rules, line)
		} else {
			update := parseUpdate(line)
			updates = append(updates, update)
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return
	}

	orderRules := parseRules(rules)

	totalSum := 0
	totalCorrectedSum := 0
	for _, update := range updates {
		if isValidUpdate(update, orderRules) {
			middle := findMiddlePage(update)
			totalSum += middle
		} else {
			// fmt.Println("us", update)
			correctedUpdate := orderUpdate(update, orderRules)
			// fmt.Println("cc", correctedUpdate, "\n")
			totalCorrectedSum += findMiddlePage(correctedUpdate)
		}
	}

	fmt.Println("Total Sum:", totalSum)
	fmt.Println("Total Corrected Sum:", totalCorrectedSum)
}

func parseRules(rules []string) map[int][]int {
	ruleMap := make(map[int][]int)
	for _, rule := range rules {
		parts := strings.Split(rule, "|")
		x, _ := strconv.Atoi(parts[0])
		y, _ := strconv.Atoi(parts[1])
		ruleMap[x] = append(ruleMap[x], y)
	}
	return ruleMap
}

func parseUpdate(line string) []int {
	parts := strings.Split(line, ",")
	var update []int
	for _, part := range parts {
		num, _ := strconv.Atoi(strings.TrimSpace(part))
		update = append(update, num)
	}
	return update
}

func isValidUpdate(update []int, rules map[int][]int) bool {
	position := make(map[int]int)
	for i, page := range update {
		position[page] = i
	}

	for x, ys := range rules {
		for _, y := range ys {
			posX, existsX := position[x]
			posY, existsY := position[y]
			if existsX && existsY && posX >= posY {
				return false
			}
		}
	}
	return true
}

func orderUpdate(update []int, rules map[int][]int) []int {
	// we have overkill topological sort here, fuck yeah.

	graph := make(map[int][]int)
	inDegree := make(map[int]int)
	pageSet := make(map[int]bool)

	for _, page := range update {
		pageSet[page] = true
		inDegree[page] = 0
	}

	for x, ys := range rules {
		if !pageSet[x] {
			continue
		}
		for _, y := range ys {
			if pageSet[y] {
				graph[x] = append(graph[x], y)
				inDegree[y]++
			}
		}
	}

	var ordered []int
	queue := []int{}

	for _, page := range update {
		if inDegree[page] == 0 {
			queue = append(queue, page)
		}
	}

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]
		ordered = append(ordered, current)

		for _, neighbor := range graph[current] {
			inDegree[neighbor]--
			if inDegree[neighbor] == 0 {
				queue = append(queue, neighbor)
			}
		}
	}

	if len(ordered) != len(update) {
		fmt.Println("len corrected doesn't match", len(ordered), len(update))
		return nil
	}

	return ordered
}

func findMiddlePage(update []int) int {
	mid := len(update) / 2
	return update[mid]
}
