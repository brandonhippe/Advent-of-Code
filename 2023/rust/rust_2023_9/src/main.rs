use relative_path::RelativePath;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let mut sum: i64 = 0;
    for line in contents.lines() {
        let nums: Vec<i64> = line
            .split_whitespace()
            .map(|s| s.parse::<i64>().unwrap())
            .collect();

        sum += extrapolate(nums, true);
    }

    return sum;
}

fn part2(contents: String) -> i64 {
    let mut sum: i64 = 0;
    for line in contents.lines() {
        let nums: Vec<i64> = line
            .split_whitespace()
            .map(|s| s.parse::<i64>().unwrap())
            .collect();

        sum += extrapolate(nums, false);
    }

    return sum;
}

fn extrapolate(nums: Vec<i64>, end: bool) -> i64 {
    if HashSet::<i64>::from_iter(nums.clone()).len() == 1 {
        return nums[0];
    }

    let mut new_nums: Vec<i64> = Vec::new();

    for i in 1..nums.len() {
        new_nums.push(nums[i] - nums[i - 1]);
    }

    return if end {
        nums.last().unwrap() + extrapolate(new_nums, end)
    } else {
        nums[0] - extrapolate(new_nums, end)
    };
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 114);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 2);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2023_9") {
        RelativePath::new("../../Inputs/2023_9.txt")
    } else {
        RelativePath::new("/Inputs/2023_9.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nSum of extrapolated values: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nSum of extrapolated values: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
