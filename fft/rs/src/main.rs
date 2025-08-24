use fft::{Complex, fft};
use std::f64::consts::PI;

fn round(n: f64) -> f64 {
    // precision = 2
    (n * 100.0).round() / 100.0
}

fn generate_inputs(len: usize) -> Vec<Complex> {
    let mut res = Vec::with_capacity(len);
    for i in 0..len {
        let theta = i as f64 / len as f64 * PI;
        let re = 1.0 * (10.0 * theta).cos() + 0.5 * (25.0 * theta).cos();
        let im = 1.0 * (10.0 * theta).sin() + 0.5 * (25.0 * theta).sin();
        res.push(Complex::new(round(re), round(im)));
    }
    res
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let size = args[1].parse::<usize>().unwrap();
    let mut signals = generate_inputs(1 << size);
    let start = std::time::Instant::now();
    fft(&mut signals);
    let end = std::time::Instant::now();

    if args.len() > 2 {
        let content = std::fs::read_to_string(args[2].clone()).unwrap();
        let input = content
            .lines()
            .map(|l| {
                let (re, im) = l.split_once(',').unwrap();
                let re = re.parse::<f64>().unwrap();
                let im = im.parse::<f64>().unwrap();
                Complex::new(re, im)
            })
            .collect::<Vec<_>>();
        for (i, signal) in signals.iter().enumerate() {
            let expected = input[i];
            assert_eq!(signal, &expected);
        }
    } else {
        println!(
            "execution time: {} ms",
            end.duration_since(start).as_millis()
        );
    }
}
