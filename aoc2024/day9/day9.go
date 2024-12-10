package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strconv"
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

	scanner := bufio.NewScanner(file)
	scanner.Scan()
	diskMap := scanner.Text()

	// part 1
	blocks := parseDiskMap(diskMap)
	start := time.Now()
	compactDisk(blocks)
	checksum := calculateChecksum(blocks)
	end1 := time.Since(start)

	// part 2
	blocks = parseDiskMap(diskMap)
	start = time.Now()
	compactDiskWholeFiles(blocks)
	checksum2 := calculateChecksum(blocks)
	end2 := time.Since(start)

	fmt.Println("Part 1 CheckSum:", checksum, "with time:", end1)
	fmt.Println("Part 2 CheckSum:", checksum2, "with time:", end2)

}

func parseDiskMap(diskMap string) []rune {
	var blocks []rune
	id := 0

	for i, c := range diskMap {
		length, _ := strconv.Atoi(string(c))

		isFile := i%2 == 0
		for j := 0; j < length; j++ {
			if isFile {
				blocks = append(blocks, rune('0'+id))
			} else {
				blocks = append(blocks, '.')
			}
		}
		if isFile {
			id++
		}
	}

	return blocks
}

func compactDisk(blocks []rune) {
	n := len(blocks)
	j := 1
	for i := n - 1; i >= 0; i-- {
		if blocks[i] != '.' {
			for j < i {
				if blocks[j] == '.' {
					blocks[j] = blocks[i]
					blocks[i] = '.'
					break
				}
				j++
			}
		}
	}
}

func compactDiskWholeFiles(blocks []rune) {
	whereFiles := make(map[int][2]int)
	maxID := 0
	ind := 0
	for ind < len(blocks)-1 {
		if blocks[ind] != '.' {
			id := int(blocks[ind] - '0')
			start := ind
			for ind < len(blocks) && int(blocks[ind]-'0') == id {
				ind++
				// if ind == len(blocks)-1 {
				// break
				// }
			}
			end := ind
			whereFiles[id] = [2]int{start, end}

			if id > maxID {
				maxID = id
			}
			continue
		}
		ind++
	}

	for id := maxID; id >= 0; id-- {
		size, _ := whereFiles[id]
		start, end := size[0], size[1]

		fileSize := end - start

		freeStart, freeSize := -1, 0
		for i := 0; i < start; i++ {
			if blocks[i] == '.' {
				if freeStart == -1 {
					freeStart = i
				}
				freeSize++
				if freeSize >= fileSize {
					for j := 0; j < fileSize; j++ {
						blocks[freeStart+j] = rune('0' + id)
						blocks[start+j] = '.'
					}
					maxID--
					break
				}
			} else {
				freeStart, freeSize = -1, 0
			}
		}
	}
}

func calculateChecksum(blocks []rune) int {
	checksum := 0
	for i, block := range blocks {
		if block != '.' {
			id := int(block - '0')
			checksum += i * id
		}
	}
	return checksum
}
