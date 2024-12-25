use relative_path::RelativePath;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    for i in 3..contents.len() {
        let sub_set: HashSet<char> = HashSet::from_iter(&mut contents[i - 3..i + 1].chars());

        if sub_set.len() == 4 {
            return i as i32 + 1;
        }
    }

    return -1;
}

fn part2(contents: String) -> i32 {
    for i in 13..contents.len() {
        let sub_set: HashSet<char> = HashSet::from_iter(&mut contents[i - 13..i + 1].chars());

        if sub_set.len() == 14 {
            return i as i32 + 1;
        }
    }

    return -1;
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

        assert_eq!(part2(contents), 19);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2022_6") {
        RelativePath::new("../../../Inputs/2022_6.txt")
    } else {
        RelativePath::new("/Inputs/2022_6.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nCharacters before start of packet: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nCharacters before start of message: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}