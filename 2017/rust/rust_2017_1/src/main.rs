use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    return contents
        .chars()
        .collect::<Vec<_>>()
        .windows(2)
        .filter(|w| w[0] == w[1])
        .map(|w| w[0].to_digit(10).unwrap() as i64)
        .sum::<i64>()
        + (if contents.chars().next().unwrap() == contents.chars().last().unwrap() {
            contents.chars().next().unwrap().to_digit(10).unwrap() as i64
        } else {
            0
        });
}

fn part2(contents: String) -> i64 {
    return contents
        .chars()
        .enumerate()
        .filter(|(i, c)| {
            c == &contents
                .chars()
                .nth((i + contents.len() / 2) % contents.len())
                .unwrap()
        })
        .map(|(i, c)| c.to_digit(10).unwrap() as i64)
        .sum::<i64>();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let mut contents = "1122".to_string();
        assert_eq!(part1(contents), 3);
        contents = "1111".to_string();
        assert_eq!(part1(contents), 4);
        contents = "1234".to_string();
        assert_eq!(part1(contents), 0);
        contents = "91212129".to_string();
        assert_eq!(part1(contents), 9);
    }

    #[test]
    fn p2_test() {
        let mut contents = "1212".to_string();
        assert_eq!(part2(contents), 6);
        contents = "1221".to_string();
        assert_eq!(part2(contents), 0);
        contents = "123425".to_string();
        assert_eq!(part2(contents), 4);
        contents = "123123".to_string();
        assert_eq!(part2(contents), 12);
        contents = "12131415".to_string();
        assert_eq!(part2(contents), 4);
    }
}

fn main() {
    let year = "2017".to_string();
    let day = "1".to_string();

    let root = env::current_dir().unwrap();
    let path_str = if root.ends_with(format!("rust_{}_{}", year, day)) {
        format!("../../../Inputs/{}_{}.txt", year, day)
    } else {
        format!("/Inputs/{}_{}.txt", year, day)
    };

    let relative_path = RelativePath::new(&path_str);

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nCaptcha solution: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nCaptcha solution: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}