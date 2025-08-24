use std::f64::consts::PI;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Complex {
    pub real: f64,
    pub imag: f64,
}

impl Complex {
    pub fn new(real: f64, imag: f64) -> Self {
        Self { real, imag }
    }
}

impl std::ops::Add for Complex {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self {
            real: self.real + other.real,
            imag: self.imag + other.imag,
        }
    }
}

impl std::ops::Sub for Complex {
    type Output = Self;

    fn sub(self, other: Self) -> Self {
        Self {
            real: self.real - other.real,
            imag: self.imag - other.imag,
        }
    }
}

impl std::ops::Mul for Complex {
    type Output = Self;

    fn mul(self, other: Self) -> Self {
        Self {
            real: self.real * other.real - self.imag * other.imag,
            imag: self.real * other.imag + self.imag * other.real,
        }
    }
}

impl std::ops::Mul<f64> for Complex {
    type Output = Self;

    fn mul(self, scalar: f64) -> Self {
        Self {
            real: self.real * scalar,
            imag: self.imag * scalar,
        }
    }
}

pub fn fft(arr: &mut [Complex]) {
    fn _fft(arr: &mut [Complex]) {
        let n = arr.len();
        if n == 1 {
            return;
        }

        let mut a0 = Vec::with_capacity(n / 2);
        let mut a1 = Vec::with_capacity(n / 2);

        for i in 0..n / 2 {
            a0.push(arr[2 * i]);
            a1.push(arr[2 * i + 1]);
        }

        _fft(&mut a0);
        _fft(&mut a1);

        let ang = -2.0 * PI / n as f64;
        let mut w = Complex::new(1.0, 0.0);
        let wn = Complex::new(ang.cos(), ang.sin());

        for i in 0..n / 2 {
            let p = a0[i];
            let q = w * a1[i];
            arr[i] = p + q;
            arr[i + n / 2] = p - q;
            w = w * wn;
        }
    }

    _fft(arr);
    let factor = 1.0 / (arr.len() as f64).sqrt();
    for it in arr {
        *it = *it * factor;
    }
}
