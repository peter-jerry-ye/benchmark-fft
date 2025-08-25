package fft

type Complex struct {
	Real, Imag float64
}

func (c Complex) Add(other Complex) Complex {
	return Complex{c.Real + other.Real, c.Imag + other.Imag}
}

func (c Complex) Sub(other Complex) Complex {
	return Complex{c.Real - other.Real, c.Imag - other.Imag}
}

func (c Complex) Mul(other Complex) Complex {
	return Complex{c.Real*other.Real - c.Imag*other.Imag, c.Real*other.Imag + c.Imag*other.Real}
}

func (c Complex) MulScalar(scalar float64) Complex {
	return Complex{c.Real * scalar, c.Imag * scalar}
}
