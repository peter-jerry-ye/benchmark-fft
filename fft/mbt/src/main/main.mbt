///|
typealias @lib.Complex

///|
fn main {
  let cli_args = @sys.get_cli_args()
  let size = try! @strconv.parse_int(cli_args[1])
  let signals = generate_inputs(1 << size)
  let start = @uv.hrtime()
  @lib.fft(signals)
  let end = @uv.hrtime()
  println("execution time: \{(end - start).to_double() / 1_000_000} ms")
  for signal in signals {
    ignore(signal)
  }
}

///|
fn round(n : Double) -> Double {
  // precision = 2
  (n * 100.0).round() / 100.0
}

///|
fn generate_inputs(len : Int) -> FixedArray[Complex] {
  let res : FixedArray[Complex] = FixedArray::make(len, Complex::{
    real: 0.0,
    imag: 0.0,
  })
  for i in 0..<len {
    let theta = i.to_double() / len.to_double() * @math.PI
    let re = 1.0 * @math.cos(10.0 * theta) + 0.5 * @math.cos(25.0 * theta)
    let im = 1.0 * @math.sin(10.0 * theta) + 0.5 * @math.sin(25.0 * theta)
    res[i] = Complex::{ real: round(re), imag: round(im) }
  }
  res
}
