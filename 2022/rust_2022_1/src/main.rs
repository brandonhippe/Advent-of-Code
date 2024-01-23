use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let mut elves: Vec<i32> = Vec::new();
    let mut curr_elf = 0;
    for line in contents.lines() {
        if line.len() == 0 {
            elves.push(curr_elf);
            curr_elf = 0;
        } else {
            curr_elf += line.parse::<i32>().unwrap();
        }
    }

    elves.push(curr_elf);
    return *elves.iter().max().unwrap();
}

fn part2(contents: String) -> i32 {
    let mut elves: Vec<i32> = Vec::new();
    let mut curr_elf = 0;
    for line in contents.lines() {
        if line.len() == 0 {
            elves.push(curr_elf);
            curr_elf = 0;
        } else {
            curr_elf += line.parse::<i32>().unwrap();
        }
    }

    elves.push(curr_elf);
    elves.sort();
    return elves[elves.len() - 3..elves.len()].iter().sum();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 24000);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 45000);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2022_1") {
        RelativePath::new("../../Inputs/2022_1.txt")
    } else {
        RelativePath::new("/Inputs/2022_1.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nMost calories: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nSum of 3 most calories: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
