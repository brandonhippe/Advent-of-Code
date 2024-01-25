use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let nums: Vec<i32> = contents
        .split(",")
        .map(|x| x.parse::<i32>().unwrap())
        .collect();

    let min: i32 = *nums.iter().min().unwrap();
    let max: i32 = *nums.iter().max().unwrap();

    return (min..max + 1)
        .map(|c| nums.iter().map(|n| (n - c).abs()).sum::<i32>())
        .min()
        .unwrap();
}

fn part2(contents: String) -> i32 {
    let nums: Vec<i32> = contents
        .split(",")
        .map(|x| x.parse::<i32>().unwrap())
        .collect();

    let min: i32 = *nums.iter().min().unwrap();
    let max: i32 = *nums.iter().max().unwrap();

    return (min..max + 1)
        .map(|c| {
            nums.iter()
                .map(|n| ((n - c).abs()) * ((n - c).abs() + 1) / 2)
                .sum::<i32>()
        })
        .min()
        .unwrap();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 37);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 168);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2021_7") {
        RelativePath::new("../../Inputs/2021_7.txt")
    } else {
        RelativePath::new("/Inputs/2021_7.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nMinimum fuel: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nMinimun fuel: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
