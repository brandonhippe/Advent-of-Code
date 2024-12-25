use itertools::Itertools;
use relative_path::RelativePath;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    return galaxy_dist(contents, 2) as i32;
}

fn part2(contents: String, mult: i64) -> i64 {
    return galaxy_dist(contents, mult);
}

fn galaxy_dist(contents: String, mult: i64) -> i64 {
    let mut galaxies: Vec<(i32, i32)> = Vec::new();
    let mut empty_rows: HashSet<i32> =
        HashSet::from_iter((0..contents.lines().count()).map(|x| x as i32));
    let mut empty_cols: HashSet<i32> = HashSet::from_iter(
        (0..contents.lines().nth(0).expect("").chars().count()).map(|x| x as i32),
    );

    for (y, line) in contents.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                galaxies.push((x as i32, y as i32));

                if empty_rows.contains(&(y as i32)) {
                    empty_rows.remove(&(y as i32));
                }

                if empty_cols.contains(&(x as i32)) {
                    empty_cols.remove(&(x as i32));
                }
            }
        }
    }

    let mut sum: i64 = 0;

    for ((a1, a2), (b1, b2)) in galaxies.iter().cartesian_product(galaxies.iter()) {
        let min_x = std::cmp::min(a1, b1);
        let max_x = std::cmp::max(a1, b1);
        let min_y = std::cmp::min(a2, b2);
        let max_y = std::cmp::max(a2, b2);

        let expand_x: i64 = empty_cols
            .iter()
            .filter(|x| *x >= min_x && *x <= max_x)
            .count() as i64;
        let expand_y: i64 = empty_rows
            .iter()
            .filter(|y| *y >= min_y && *y <= max_y)
            .count() as i64;

        sum += (a1 - b1).abs() as i64
            + (expand_x * (mult - 1))
            + (a2 - b2).abs() as i64
            + (expand_y * (mult - 1));
    }

    return sum / 2;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 374);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents.clone(), 10), 1030);
        assert_eq!(part2(contents, 100), 8410);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2023_11") {
        RelativePath::new("../../../Inputs/2023_11.txt")
    } else {
        RelativePath::new("/Inputs/2023_11.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nSum of distances between expanded galaxies: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nSum of distances between expanded galaxies: {}\nRan in {:.5?}",
        part2(contents.clone(), 1_000_000),
        part2_timer.elapsed()
    );
}