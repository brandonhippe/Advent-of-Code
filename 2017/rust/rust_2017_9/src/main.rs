use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let mut score = 0;
    for line in contents.lines() {
        let mut contain_score = 0;
        let mut escaped = false;
        let mut in_garbage = false;

        for c in line.chars() {
            if escaped {
                escaped = false;
            } else if in_garbage {
                match c {
                    '!' => escaped = true,
                    '>' => in_garbage = false,
                    _ => {}
                }
            } else {
                match c {
                    '!' => escaped = true,
                    '{' => {
                        contain_score += 1;
                    }
                    '}' => {
                        score += contain_score;
                        contain_score -= 1;
                    }
                    '<' => in_garbage = true,
                    _ => {}
                }
            }
        }
    }

    return score;
}

fn part2(contents: String) -> i64 {
    let mut total = 0;
    for line in contents.lines() {
        let mut escaped = false;
        let mut in_garbage = false;

        for c in line.chars() {
            if escaped {
                escaped = false;
            } else {
                total += in_garbage as i64;
                match c {
                    '!' => {
                        escaped = true;
                        total -= in_garbage as i64;
                    }
                    '<' => in_garbage = true,
                    '>' => {
                        total -= in_garbage as i64;
                        in_garbage = false;
                    }
                    _ => {}
                }
            }
        }
    }

    return total;
}

fn main() {
    let year = "2017".to_string();
    let day = "9".to_string();

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
        "\nPart 1:\nTotal score for all groups: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nNon-cancelled characters in garbage: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
