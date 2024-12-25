use relative_path::RelativePath;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    return polymer_len(contents);
}

fn part2(contents: String) -> i64 {
    let char_set = contents
        .chars()
        .map(|c| c.to_ascii_lowercase())
        .collect::<HashSet<char>>();
    let mut min_len = std::i64::MAX;
    for c in char_set {
        let len = polymer_len(contents.replace(c, "").replace(c.to_ascii_uppercase(), ""));
        if len < min_len {
            min_len = len;
        }
    }

    return min_len;
}

fn polymer_len(contents: String) -> i64 {
    let mut stack = Vec::new();
    for c in contents.chars() {
        if stack.len() == 0 {
            stack.push(c);
        } else {
            let last = stack.pop().unwrap();
            if last.to_ascii_lowercase() == c.to_ascii_lowercase() && last != c {
                continue;
            } else {
                stack.push(last);
                stack.push(c);
            }
        }
    }

    return stack.len() as i64;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 10);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 4);
    }
}

fn main() {
    let year = "2018".to_string();
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
        "\nPart 1:\nLength of polymer: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nShortest polymer: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
