package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
)

func main() {
	args := flag.Bool("example", false, "example or input, just type the '-example' for example")
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
	dial := 50
	zero_times := 0
	cross_zero_times := 0
	was_zero := false

	for {
		instruction, _, _ := reader.ReadLine()
		if len(instruction) == 0 {
			break
		}
		direction := string(instruction[0])
		amount, _ := strconv.Atoi(string(instruction[1:]))

		if amount > 100 {
			cross_zero_times += amount / 100
			amount = amount % 100
		}
		switch direction {
		case "R":
			dial = dial + amount
			if dial > 100 {
				cross_zero_times += 1
			}
		case "L":
			dial = dial - amount
			if (dial < 0) && !was_zero {
				dial = 100 + dial
				cross_zero_times += 1
			}
		}
		dial = (dial%100 + 100) % 100
		fmt.Println(dial)
		if dial == 0 {
			zero_times += 1
			was_zero = true
		} else {
			was_zero = false
		}
	}
	fmt.Println("Zero Times", zero_times)
	fmt.Println("Cross Zero Times and Sum", cross_zero_times, cross_zero_times+zero_times)
}
