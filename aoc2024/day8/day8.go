package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"time"
)

var grid []string

func main() {
	example := flag.Bool("example", false, "example or input")
	print := flag.Bool("print", false, "verbose")
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

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		grid = append(grid, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return
	}

	antennas := findAntennas(grid)

	// part 1
	start := time.Now()
	antinodes := generateAntinodes(grid, antennas, true)
	end1 := time.Since(start)
	if *print {
		for p := range antinodes {
			grid[p[1]] = replaceCharAt(grid[p[1]], p[0], '#')
		}
		for _, line := range grid {
			fmt.Println(line)
		}
	}
	fmt.Println("Total antinodes:", len(antinodes), "with time:", end1)

	// part 2
	start = time.Now()
	antinodes2 := generateAntinodes(grid, antennas, false)
	end2 := time.Since(start)
	if *print {
		for p := range antinodes2 {
			grid[p[1]] = replaceCharAt(grid[p[1]], p[0], '#')
		}
		for _, line := range grid {
			fmt.Println(line)
		}
	}
	for _, anantenna := range antennas {
		for _, point := range anantenna {
			antinodes2[point] = true
		}
	}
	fmt.Println("Total antinodes inline:", len(antinodes2), "with time:", end2)

}

func findAntennas(grid []string) map[rune][][2]int {
	antennas := make(map[rune][][2]int)
	for y, row := range grid {
		for x, cell := range row {
			if cell != '.' {
				antennas[rune(cell)] = append(antennas[rune(cell)], [2]int{x, y})
			}
		}
	}
	return antennas
}

func generateAntinodes(grid []string, antennas map[rune][][2]int, ones bool) map[[2]int]bool {
	antinodes := make(map[[2]int]bool)
	height := len(grid)
	width := len(grid[0])

	for _, positions := range antennas {
		for i := 0; i < len(positions); i++ {
			for j := i + 1; j < len(positions); j++ {
				x1, y1 := positions[i][0], positions[i][1]
				x2, y2 := positions[j][0], positions[j][1]

				dx, dy := x2-x1, y2-y1

				addAntinodes(antinodes, x2, dx, y2, dy, width, height, ones)
				addAntinodes(antinodes, x1, -dx, y1, -dy, width, height, ones)
			}
		}
	}

	return antinodes
}

func addAntinodes(antinodes map[[2]int]bool, x, dx, y, dy, width, height int, ones bool) {
	ax, ay := x+dx, y+dy
	for {
		if ax >= 0 && ax < width && ay >= 0 && ay < height {
			antinodes[[2]int{ax, ay}] = true
			ax, ay = ax+dx, ay+dy
			if ones {
				break
			}
		} else {
			break
		}
	}
}

func replaceCharAt(s string, index int, newChar rune) string {
	runes := []rune(s)
	runes[index] = newChar
	return string(runes)
}
