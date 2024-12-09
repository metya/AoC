package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"slices"
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
	reader := bufio.NewReader(file)
	for {
		line, _, _ := reader.ReadLine()
		if len(line) == 0 {
			break
		}
		grid = append(grid, string(line))
	}

	rows := len(grid)
	cols := len(grid[0])

	xmas := "XMAS"
	mas := "MAS"

	directions := [][2]int{
		{0, 1},   // →
		{0, -1},  // ←
		{-1, 0},  // ↓
		{1, 0},   // ↑
		{1, 1},   // ↘
		{-1, -1}, // ↖
		{-1, 1},  // ↗
		{1, -1},  // ↙
	}

	uniqueWords := make(map[[3]int]bool) // [row, col, directionIndex]

	isXMAS := func(startRow, startCol, dirX, dirY int) bool {
		for i := 0; i < len(xmas); i++ {
			newRow := startRow + i*dirX
			newCol := startCol + i*dirY
			if newRow < 0 || newRow >= rows || newCol < 0 || newCol >= cols || grid[newRow][newCol] != xmas[i] {
				return false
			}
		}
		return true
	}

	isMAS := func(diagonal []byte) bool {
		line := string(diagonal)
		slices.Reverse(diagonal)
		return line == mas || string(diagonal) == mas
	}

	totalCount := 0
	totalXmas := 0
	// part1
	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			if grid[row][col] == 'X' {
				for dirIndex, dir := range directions {
					dirX, dirY := dir[0], dir[1]
					if isXMAS(row, col, dirX, dirY) {
						key := [3]int{row, col, dirIndex}
						if !uniqueWords[key] {
							uniqueWords[key] = true
							totalCount++
						}
					}
				}
			}
		}
	}
	//part2
	for row := 1; row < rows-1; row++ {
		for col := 1; col < cols-1; col++ {
			if grid[row][col] == 'A' {
				// ↘
				diagonal1 := []byte{
					grid[row-1][col-1],
					grid[row][col],
					grid[row+1][col+1],
				}
				// ↖
				diagonal2 := []byte{
					grid[row+1][col-1],
					grid[row][col],
					grid[row-1][col+1],
				}

				if isMAS(diagonal1) && isMAS(diagonal2) {
					totalXmas++
				}
			}
		}
	}
	fmt.Println("Total count of XMAS:", totalCount)
	fmt.Println("Total count of X-MAS:", totalXmas)
}
