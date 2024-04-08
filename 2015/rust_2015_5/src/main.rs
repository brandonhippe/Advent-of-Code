use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;
use fancy_regex::Regex;

fn part1(contents: String) -> i64 {
    let vowel_re: Regex = Regex::new(r"([aeiou])").unwrap();
    let bad_re: Regex = Regex::new(r"(ab|cd|pq|xy)").unwrap();
    let double_re: Regex = Regex::new(r"(.)\1").unwrap();
    return contents
        .lines()
        .map(|line| {
            if !bad_re.is_match(line).unwrap() && vowel_re.find_iter(line).count() >= 3 && double_re.is_match(line).unwrap() {
                return 1;
            }
            return 0;
        })
        .sum::<i64>();
}

fn part2(contents: String) -> i64 {
    let pair_re: Regex = Regex::new(r"(.{2}).*\1").unwrap();
    let repeat_re: Regex = Regex::new(r"(.).\1").unwrap();
    return contents
        .lines()
        .map(|line| {
            if pair_re.is_match(line).unwrap() && repeat_re.is_match(line).unwrap() {
                return 1;
            }
            return 0;
        })
        .sum::<i64>()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 0);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 0);
    }
}

fn main() {
    let year = "2015".to_string();
    let day = "5".to_string();

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
        "\nPart 1:\nNice Strings: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nNice Strings: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
