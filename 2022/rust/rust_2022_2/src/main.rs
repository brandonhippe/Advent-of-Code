use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let games: Vec<(i32, i32)> = contents
        .lines()
        .map(|line| {
            (
                line.chars().nth(0).unwrap() as i32 - 'A' as i32,
                line.chars().nth(2).unwrap() as i32 - 'X' as i32,
            )
        })
        .collect();

    return games
        .iter()
        .map(|(other, you)| ((you - other + 4) % 3) * 3 + (you + 1))
        .sum();
}

fn part2(contents: String) -> i32 {
    let games: Vec<(i32, i32)> = contents
        .lines()
        .map(|line| {
            (
                line.chars().nth(0).unwrap() as i32 - 'A' as i32,
                line.chars().nth(2).unwrap() as i32 - 'X' as i32,
            )
        })
        .collect();

    return games
        .iter()
        .map(|(other, res)| {
            let you = (other + res + 2) % 3;
            ((you - other + 4) % 3) * 3 + (you + 1)
        })
        .sum();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 15);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 12);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2022_2") {
        RelativePath::new("../../../Inputs/2022_2.txt")
    } else {
        RelativePath::new("/Inputs/2022_2.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nScore: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nScore: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}