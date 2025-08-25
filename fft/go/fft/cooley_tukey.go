package fft

import "math"

func FFT(arr []Complex) {
	fft(arr)
	factor := 1.0 / math.Sqrt(float64(len(arr)))
	for i := range len(arr) {
		arr[i] = arr[i].MulScalar(factor)
	}
}

func fft(arr []Complex) {
	n := len(arr)
	if n == 1 {
		return
	}

	a0 := make([]Complex, 0, n/2)
	a1 := make([]Complex, 0, n/2)
	for i := range n / 2 {
		a0 = append(a0, arr[2*i])
		a1 = append(a1, arr[2*i+1])
	}

	fft(a0)
	fft(a1)

	ang := -2 * math.Pi / float64(n)
	w := Complex{1, 0}
	wn := Complex{math.Cos(ang), math.Sin(ang)}
	for i := range n / 2 {
		p := a0[i]
		q := w.Mul(a1[i])
		arr[i] = p.Add(q)
		arr[i+n/2] = p.Sub(q)
		w = w.Mul(wn)
	}
}
