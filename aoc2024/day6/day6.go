package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
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

	var grid []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		grid = append(grid, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return
	}

	startX, startY, direction := findStart(grid)

	start := time.Now()
	_, visited := simulate(grid, startX, startY, direction)
	lenv := make(map[[2]int]bool)
	for x := range visited {
		lenv[[2]int{x[0], x[1]}] = true
	}
	part1_time := time.Since(start)
	start = time.Now()
	loopPositions := findLoopObstacles(grid, [3]int{startX, startY, directionIndex(direction)}, visited)
	part2_time := time.Since(start)
	fmt.Println("Visited Distinct Positions:", len(lenv), "in time:", part1_time)
	fmt.Println("Loop Positions:", len(loopPositions), "in time:", part2_time)
}

func findStart(grid []string) (int, int, string) {
	for y, row := range grid {
		for x, cell := range row {
			switch cell {
			case '^':
				return x, y, "up"
			case '>':
				return x, y, "right"
			case '<':
				return x, y, "left"
			case 'v':
				return x, y, "down"
			}
		}
	}
	return -1, -1, ""
}

func simulate(grid []string, startX, startY int, direction string) (bool, map[[3]int]bool) {
	visited := make(map[[3]int]bool)
	directions := map[string][2]int{
		"up":    {0, -1},
		"right": {1, 0},
		"down":  {0, 1},
		"left":  {-1, 0},
	}
	turnRight := map[string]string{
		"up":    "right",
		"right": "down",
		"down":  "left",
		"left":  "up",
	}

	x, y := startX, startY
	visited[[3]int{x, y, directionIndex(direction)}] = true

	for {
		dx, dy := directions[direction][0], directions[direction][1]
		nextX, nextY := x+dx, y+dy

		if nextY < 0 || nextY >= len(grid) || nextX < 0 || nextX >= len(grid[nextY]) {
			return false, visited
		}

		if grid[nextY][nextX] == '#' {
			direction = turnRight[direction]
		} else {
			x, y = nextX, nextY
		}

		state := [3]int{x, y, directionIndex(direction)}
		if visited[state] {
			return true, visited
		}
		visited[state] = true
	}

}

func findLoopObstacles(grid []string, start [3]int, visited map[[3]int]bool) map[[2]int]bool {

	originalGrid := make([]string, len(grid))
	copy(originalGrid, grid)

	loopPositions := make(map[[2]int]bool)

	for point := range visited {
		x, y, _ := point[0], point[1], point[2]
		if x == start[0] && y == start[1] {
			continue
		}

		gridCopy := make([]string, len(originalGrid))
		copy(gridCopy, originalGrid)
		gridCopy[y] = replaceCharAt(gridCopy[y], x, '#')

		cycle, _ := simulate(gridCopy,
			// x-indexPairDirection(direction)[0],
			// y-indexPairDirection(direction)[1],
			// indexDirection(direction+1),
			start[0],
			start[1],
			indexDirection(start[2]),
		)
		if cycle {
			loopPositions[[2]int{x, y}] = true
		}
	}

	return loopPositions
}

func replaceCharAt(s string, index int, newChar rune) string {
	runes := []rune(s)
	runes[index] = newChar
	return string(runes)
}

func directionIndex(direction string) int {
	switch direction {
	case "up":
		return 0
	case "right":
		return 1
	case "down":
		return 2
	case "left":
		return 3
	}
	return -1
}

func indexDirection(direction int) string {
	switch direction % 4 {
	case 0:
		return "up"
	case 1:
		return "right"
	case 2:
		return "down"
	case 3:
		return "left"
	}
	return ""
}

func indexPairDirection(direction int) [2]int {
	switch direction {
	case 0:
		return [2]int{0, -1}
	case 1:
		return [2]int{1, 0}
	case 2:
		return [2]int{0, 1}
	case 3:
		return [2]int{-1, 0}
	}
	return [2]int{0, 0}
}
