use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> String {
    let mut occurances: Vec<Vec<i64>> = Vec::new();

    for line in contents.lines() {
        for (i, c) in line.chars().enumerate() {
            while occurances.len() <= i {
                occurances.push(vec![0; 26]);
            }

            occurances[i][c as usize - 'a' as usize] += 1;
        }
    }

    return occurances
        .iter()
        .map(|x| {
            let mut max = 0;
            let mut max_index = 0;
            for (i, &count) in x.iter().enumerate() {
                if count > max {
                    max = count;
                    max_index = i;
                }
            }

            return (max_index + 'a' as usize) as u8 as char;
        })
        .collect();
}

fn part2(contents: String) -> String {
    let mut occurances: Vec<Vec<i64>> = Vec::new();

    for line in contents.lines() {
        for (i, c) in line.chars().enumerate() {
            while occurances.len() <= i {
                occurances.push(vec![0; 26]);
            }

            occurances[i][c as usize - 'a' as usize] += 1;
        }
    }

    return occurances
        .iter()
        .map(|x| {
            let mut min = i64::MAX;
            let mut min_index = 0;
            for (i, &count) in x.iter().enumerate() {
                if count != 0 && count < min {
                    min = count;
                    min_index = i;
                }
            }

            return (min_index + 'a' as usize) as u8 as char;
        })
        .collect();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), "easter".to_string());
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), "advent".to_string());
    }
}

fn main() {
    let year = "2016".to_string();
    let day = "6".to_string();

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
        "\nPart 1:\nError corrected message: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nError corrected message: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
