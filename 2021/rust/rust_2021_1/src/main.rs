use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let lines: Vec<_> = contents.lines().collect();
    let mut prev = lines[0].parse::<i32>().unwrap();

    let mut increased = 0;
    for line in lines.iter().skip(1) {
        let num = line.parse::<i32>().unwrap();

        if num > prev {
            increased += 1;
        }

        prev = num;
    }

    return increased;
}

fn part2(contents: String) -> i32 {
    let nums = contents
        .lines()
        .map(|line| line.parse::<i32>().unwrap())
        .collect::<Vec<_>>();

    let mut window: i32 = nums[0..3].iter().sum();
    let mut increased = 0;
    for n in 0..nums.len() - 3 {
        let prev = window;
        window = window - nums[n] + nums[n + 3];

        if window > prev {
            increased += 1;
        }
    }

    return increased;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 7);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 5);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2021_1") {
        RelativePath::new("../../../Inputs/2021_1.txt")
    } else {
        RelativePath::new("/Inputs/2021_1.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nNumber of measurements larger than previous: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nNumber of windows larger than previous: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}