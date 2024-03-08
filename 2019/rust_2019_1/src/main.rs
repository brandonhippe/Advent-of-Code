use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    return fuel_required(
        contents
            .lines()
            .map(|line| line.parse::<i64>().unwrap())
            .collect(),
    )
    .iter()
    .sum();
}

fn part2(contents: String) -> i64 {
    let mut fuel: i64 = 0;
    let mut masses: Vec<i64> = contents
        .lines()
        .map(|line| line.parse::<i64>().unwrap())
        .collect();
    loop {
        let fuels = fuel_required(masses);
        if fuels.len() == 0 {
            break;
        }

        fuel += fuels.iter().sum::<i64>();
        masses = fuels;
    }

    return fuel;
}

fn fuel_required(masses: Vec<i64>) -> Vec<i64> {
    return masses
        .iter()
        .map(|m| m / 3 - 2)
        .filter(|f| *f >= 0)
        .collect();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 34241);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 51316);
    }
}

fn main() {
    let year = "2019".to_string();
    let day = "1".to_string();

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
        "\nPart 1:\nFuel Required: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nFuel Required: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
