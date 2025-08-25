public struct Complex {
  public var real: Double
  public var imag: Double

  public init(real: Double, imag: Double) {
    self.real = real
    self.imag = imag
  }
}

extension Complex {
  public static func + (l: Complex, r: Complex) -> Complex {
    return Complex(real: l.real + r.real, imag: l.imag + r.imag)
  }

  public static func - (l: Complex, r: Complex) -> Complex {
    return Complex(real: l.real - r.real, imag: l.imag - r.imag)
  }

  public static func * (l: Complex, r: Complex) -> Complex {
    return Complex(
      real: l.real * r.real - l.imag * r.imag,
      imag: l.real * r.imag + l.imag * r.real)
  }

  public static func * (l: Complex, r: Double) -> Complex {
    return Complex(real: l.real * r, imag: l.imag * r)
  }
}
