package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
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
		fmt.Println(err)
		return
	}
	defer file.Close()

	var grid [][]int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		row := []int{}
		for _, c := range line {
			row = append(row, int(c-'0'))
		}
		grid = append(grid, row)
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return
	}

	// part 1
	start := time.Now()
	totalScore := calculateTrailheadScores(grid, bfs)
	end1 := time.Since(start)

	// part 2
	start = time.Now()
	totalRating := calculateTrailheadScores(grid, countUniqueTrails)
	end2 := time.Since(start)

	fmt.Println("Sum of Trailheads:", totalScore, "with time:", end1)
	fmt.Println("Sum of Rating:", totalRating, "with time:", end2)
}

func calculateTrailheadScores(grid [][]int, bfs func([][]int, int, int) int) int {
	totalScore := 0
	for y, row := range grid {
		for x, cell := range row {
			if cell == 0 {
				score := bfs(grid, x, y)
				totalScore += score
			}
		}
	}
	return totalScore
}

func countUniqueTrails(grid [][]int, startX, startY int) int {
	height, width := len(grid), len(grid[0])
	memo := make(map[[3]int]int)

	var dfs func(x, y, prevHeight int) int
	dfs = func(x, y, prevHeight int) int {
		if x < 0 || x >= width || y < 0 || y >= height || grid[y][x] != prevHeight+1 {
			return 0
		}

		if grid[y][x] == 9 {
			return 1
		}

		state := [3]int{x, y, grid[y][x]}
		if result, found := memo[state]; found {
			return result
		}

		directions := [][2]int{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
		count := 0
		for _, d := range directions {
			nx, ny := x+d[0], y+d[1]
			count += dfs(nx, ny, grid[y][x])
		}

		memo[state] = count
		return count
	}

	return dfs(startX, startY, -1) // start with -1, to head 0
}

func bfs(grid [][]int, startX, startY int) int {
	directions := [][2]int{{0, 1}, {1, 0}, {0, -1}, {-1, 0}}
	height, width := len(grid), len(grid[0])
	visited := make(map[[2]int]bool)
	queue := [][2]int{{startX, startY}}
	visited[[2]int{startX, startY}] = true

	reachableNines := 0

	for len(queue) > 0 {
		x, y := queue[0][0], queue[0][1]
		queue = queue[1:]

		for _, d := range directions {
			nx, ny := x+d[0], y+d[1]

			if nx < 0 || nx >= width || ny < 0 || ny >= height {
				continue
			}

			if !visited[[2]int{nx, ny}] && grid[ny][nx] == grid[y][x]+1 {
				visited[[2]int{nx, ny}] = true
				queue = append(queue, [2]int{nx, ny})

				if grid[ny][nx] == 9 {
					reachableNines++
				}
			}
		}
	}

	return reachableNines
}
