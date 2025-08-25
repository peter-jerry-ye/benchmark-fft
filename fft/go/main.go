package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"time"

	f "main/fft"
)

// func main() {
// 	signals := generateInputs(16384)
// 	f.FFT(signals)
// 	for _, signal := range signals {
// 		fmt.Printf("%.2f,%.2f\n", round(signal.Real), round(signal.Imag))
// 	}
// }

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "usage: %s <size>\n", os.Args[0])
		os.Exit(1)
	}
	size, err := strconv.Atoi(os.Args[1])
	if err != nil || size < 0 {
		fmt.Fprintln(os.Stderr, "invalid <size>; must be a non-negative integer")
		os.Exit(1)
	}
	n := 1 << uint(size)

	signals := generateInputs(n)

	start := time.Now()
	f.FFT(signals) // assumes in-place transform over []Complex
	elapsed := time.Since(start)
  ms := float64(elapsed.Nanoseconds()) / 1_000_000.0
	fmt.Printf("execution time: %.3f ms\n", ms)
}

func round(n float64) float64 {
	// precision = 2
	return math.Round(n*100.0) / 100.0
}

func generateInputs(len int) []f.Complex {
	inputs := make([]f.Complex, 0, len)
	for i := range len {
		theta := (float64(i) / float64(len)) * math.Pi
		re := 1.0*math.Cos(10.0*theta) + 0.5*math.Cos(25.0*theta)
		im := 1.0*math.Sin(10.0*theta) + 0.5*math.Sin(25.0*theta)
		inputs = append(inputs, f.Complex{Real: round(re), Imag: round(im)})
	}
	return inputs
}
