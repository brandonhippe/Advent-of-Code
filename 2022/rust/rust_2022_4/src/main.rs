use itertools::Itertools;
use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let mut contained = 0;
    for line in contents.lines() {
        let (g1, g2) = line.split(",").collect_tuple().unwrap();

        let (g1_min, g1_max) = g1
            .to_string()
            .split("-")
            .map(|num| num.parse::<i32>().unwrap())
            .collect_tuple()
            .unwrap();
        let (g2_min, g2_max) = g2
            .to_string()
            .split("-")
            .map(|num| num.parse::<i32>().unwrap())
            .collect_tuple()
            .unwrap();

        if (g1_min <= g2_min && g2_max <= g1_max) || (g2_min <= g1_min && g1_max <= g2_max) {
            contained += 1;
        }
    }

    return contained;
}

fn part2(contents: String) -> i32 {
    let mut overlap = 0;
    for line in contents.lines() {
        let (g1, g2) = line.split(",").collect_tuple().unwrap();

        let (g1_min, g1_max) = g1
            .to_string()
            .split("-")
            .map(|num| num.parse::<i32>().unwrap())
            .collect_tuple()
            .unwrap();
        let (g2_min, g2_max) = g2
            .to_string()
            .split("-")
            .map(|num| num.parse::<i32>().unwrap())
            .collect_tuple()
            .unwrap();

        if (g1_min <= g2_min && g2_min <= g1_max) || (g2_min <= g1_min && g1_min <= g2_max) {
            overlap += 1;
        }
    }

    return overlap;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 2);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 4);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2022_4") {
        RelativePath::new("../../../Inputs/2022_4.txt")
    } else {
        RelativePath::new("/Inputs/2022_4.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nFully contained ranges: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nOverlapping ranges: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}