import Foundation

public func fft(_ arr: inout [Complex]) {
  func _fft(_ arr: inout [Complex]) {
    let n = arr.count
    if n == 1 {
      return
    }

    var a0 = [Complex]()
    a0.reserveCapacity(n / 2)
    var a1 = [Complex]()
    a1.reserveCapacity(n / 2)
    for i in 0..<n / 2 {
      a0.append(arr[2 * i])
      a1.append(arr[2 * i + 1])
    }

    _fft(&a0)
    _fft(&a1)

    let ang = -2.0 * Double.pi / Double(n)
    var w = Complex(real: 1, imag: 0)
    let wn = Complex(real: cos(ang), imag: sin(ang))
    for i in 0..<n / 2 {
      let p = a0[i]
      let q = w * a1[i]
      arr[i] = p + q
      arr[i + n / 2] = p - q
      w = w * wn
    }
  }

  _fft(&arr)
  let factor = 1.0 / Double(arr.count).squareRoot()
  for i in 0..<arr.count {
    arr[i] = arr[i] * factor
  }
}
