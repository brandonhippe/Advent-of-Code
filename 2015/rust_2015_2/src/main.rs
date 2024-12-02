use regex::Regex;
use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let int_re: Regex = Regex::new(r"(\d+)").unwrap();
    return contents
        .lines()
        .map(|line| {
            let mut dims: Vec<i64> = int_re
                .captures_iter(line)
                .map(|cap| cap[0].parse().unwrap())
                .collect();
            dims.sort();

            2 * (dims[0] * dims[1] + dims[1] * dims[2] + dims[2] * dims[0]) + dims[0] * dims[1]
        })
        .sum();
}

fn part2(contents: String) -> i64 {
    let int_re: Regex = Regex::new(r"(\d+)").unwrap();
    return contents
        .lines()
        .map(|line| {
            let mut dims: Vec<i64> = int_re
                .captures_iter(line)
                .map(|cap| cap[0].parse().unwrap())
                .collect();
            dims.sort();

            2 * (dims[0] + dims[1]) + dims.iter().product::<i64>()
        })
        .sum();
}

fn main() {
    let year = "2015".to_string();
    let day = "2".to_string();

    let root = env::current_dir().unwrap();
    let path_str = if root.ends_with(format!("rust_{}_{}", year, day)) {
        format!("../../Inputs/{}_{}.txt", year, day)
    } else {
        format!("/Inputs/{}_{}.txt", year, day)
    };

    let relative_path = RelativePath::new(&path_str);

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nWrapping paper needed: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nRibbon needed: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}