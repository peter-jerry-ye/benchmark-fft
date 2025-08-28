///|
/// The function implementing the Cooley–Tukey algorithm for Fast Fourier Transform (FFT), as
/// described in <https://cp-algorithms.com/algebra/fft.html#implementation>.
///
/// The input signal is modified in-place.
pub fn fft(arr : Array[Complex]) -> Unit {
  fn _fft(arr : Array[Complex]) {
    let n = arr.length()
    if n == 1 {
      return
    }
    let a0 = Array::makei(n / 2, i => arr[2 * i])
    let a1 = Array::makei(n / 2, i => arr[2 * i + 1])
    _fft(a0)
    _fft(a1)
    let ang = -2.0 * @math.PI / Double::from_int(n)
    let mut w = { real: 1.0, imag: 0.0 }
    let wn = { real: @math.cos(ang), imag: @math.sin(ang) }
    for i in 0..<(n / 2) {
      let p = a0[i]
      let q = w * a1[i]
      arr[i] = p + q
      arr[i + n / 2] = p - q
      w = w * wn
    }
  }

  _fft(arr)
  let factor = 1.0 / Double::from_int(arr.length()).sqrt()
  for i in 0..<arr.length() {
    arr[i] = arr[i].mul_scalar(factor)
  }
}
