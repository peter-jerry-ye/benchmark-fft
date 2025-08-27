///|
#valtype
pub(all) struct Complex {
  real : Double
  imag : Double
}

///|
pub impl Add for Complex with op_add(self : Complex, other : Complex) -> Complex {
  { real: self.real + other.real, imag: self.imag + other.imag }
}

///|
pub impl Sub for Complex with op_sub(self : Complex, other : Complex) -> Complex {
  { real: self.real - other.real, imag: self.imag - other.imag }
}

///|
#inline
pub impl Mul for Complex with op_mul(self : Complex, other : Complex) -> Complex {
  {
    real: self.real * other.real - self.imag * other.imag,
    imag: self.real * other.imag + self.imag * other.real,
  }
}

///|
pub fn Complex::mul_scalar(self : Complex, scalar : Double) -> Complex {
  { real: self.real * scalar, imag: self.imag * scalar }
}
