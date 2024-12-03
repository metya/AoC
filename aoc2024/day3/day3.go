package main

import (
	"flag"
	"fmt"
	"os"
	"regexp"
	"strconv"
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

	var data []byte
	data, err = os.ReadFile(file.Name())
	if err != nil {
		fmt.Println(err)
		return
	}

	// part 1

	mul := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	matches := mul.FindAllStringSubmatch(string(data), -1)

	total := 0
	for _, match := range matches {
		x, err1 := strconv.Atoi(match[1])
		y, err2 := strconv.Atoi(match[2])
		if err1 == nil && err2 == nil {
			total += x * y
		}
	}

	// part 2

	do := regexp.MustCompile(`do`)
	dont := regexp.MustCompile(`don't`)

	isEnabled := true
	totalCorrected := 0

	cursor := 0
	for cursor < len(data) {
		if dontMatch := dont.FindIndex(data[cursor:]); dontMatch != nil && dontMatch[0] == 0 {
			isEnabled = false
			cursor += dontMatch[1]
			continue
		}

		if doMatch := do.FindIndex(data[cursor:]); doMatch != nil && doMatch[0] == 0 {
			isEnabled = true
			cursor += doMatch[1]
			continue
		}

		if mulMatch := mul.FindSubmatchIndex(data[cursor:]); mulMatch != nil && mulMatch[0] == 0 {
			if isEnabled {
				x, _ := strconv.Atoi(string(data[cursor+mulMatch[2] : cursor+mulMatch[3]]))
				y, _ := strconv.Atoi(string(data[cursor+mulMatch[4] : cursor+mulMatch[5]]))
				totalCorrected += x * y
			}
			cursor += mulMatch[1]
			continue
		}
		cursor++
	}

	fmt.Println("Total mul:", total)
	fmt.Println("Corrected Total mul:", totalCorrected)
}
