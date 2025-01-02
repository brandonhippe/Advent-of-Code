use relative_path::RelativePath;
use std::collections::VecDeque;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let mut fishes: VecDeque<i64> = VecDeque::from(vec![0; 9]);

    for n in contents.split(",") {
        fishes[n.parse::<usize>().unwrap()] += 1;
    }

    for _ in 0..80 {
        let expired = fishes.pop_front().unwrap();
        fishes[6] += expired;
        fishes.push_back(expired);
    }

    return fishes.iter().sum();
}

fn part2(contents: String) -> i64 {
    let mut fishes: VecDeque<i64> = VecDeque::from(vec![0; 9]);

    for n in contents.split(",") {
        fishes[n.parse::<usize>().unwrap()] += 1;
    }

    for _ in 0..256 {
        let expired = fishes.pop_front().unwrap();
        fishes[6] += expired;
        fishes.push_back(expired);
    }

    return fishes.iter().sum();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 5934);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 26984457539);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2021_6") {
        RelativePath::new("../../../Inputs/2021_6.txt")
    } else {
        RelativePath::new("/Inputs/2021_6.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nNumber of fishes after 80 days: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nNumber of fishes after 256 days: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}