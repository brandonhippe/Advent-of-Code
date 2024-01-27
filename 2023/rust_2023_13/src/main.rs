use relative_path::RelativePath;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let mut notes_sum: i32 = 0;

    let mut pattern: HashSet<(usize, usize)> = HashSet::new();
    let mut y = 0;
    for (y_off, line) in contents.lines().enumerate() {
        if line.len() == 0 {
            notes_sum += find_reflection(pattern.clone(), 0);
            pattern = HashSet::new();
            y = 0;
            continue;
        }

        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                pattern.insert((x, y));
            }
        }

        y += 1;
    }

    if pattern.len() != 0 {
        notes_sum += find_reflection(pattern.clone(), 0);
    }

    return notes_sum;
}

fn part2(contents: String) -> i32 {
    let mut notes_sum: i32 = 0;

    let mut pattern: HashSet<(usize, usize)> = HashSet::new();
    let mut y = 0;
    for (y_off, line) in contents.lines().enumerate() {
        if line.len() == 0 {
            notes_sum += find_reflection(pattern.clone(), 1);
            pattern = HashSet::new();
            y = 0;
            continue;
        }

        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                pattern.insert((x, y));
            }
        }

        y += 1;
    }

    if pattern.len() != 0 {
        notes_sum += find_reflection(pattern.clone(), 1);
    }

    return notes_sum;
}

fn find_reflection(pattern: HashSet<(usize, usize)>, differences: usize) -> i32 {
    let min_x = pattern.iter().min_by_key(|(x, _)| x).unwrap().0;
    let max_x = pattern.iter().max_by_key(|(x, _)| x).unwrap().0;
    let min_y = pattern.iter().min_by_key(|(_, y)| y).unwrap().1;
    let max_y = pattern.iter().max_by_key(|(_, y)| y).unwrap().1;

    for x_ref in min_x + 1..=max_x {
        let max_dist = std::cmp::min(x_ref - min_x, max_x - x_ref + 1);

        let left_half = pattern
            .iter()
            .filter(|(x, _)| x < &x_ref && x_ref - x <= max_dist)
            .map(|(x, y)| (*x, *y))
            .collect::<HashSet<_>>();
        let right_half = pattern
            .iter()
            .filter(|(x, _)| x >= &x_ref && x - x_ref < max_dist)
            .map(|(x, y)| (x_ref - (x - x_ref) - 1, *y))
            .collect::<HashSet<_>>();

        if left_half.symmetric_difference(&right_half).count() == differences {
            return x_ref as i32;
        }
    }

    for y_ref in min_y + 1..=max_y {
        let max_dist = std::cmp::min(y_ref - min_y, max_y - y_ref + 1);

        let top_half = pattern
            .iter()
            .filter(|(_, y)| y < &y_ref && y_ref - y <= max_dist)
            .map(|(x, y)| (*x, *y))
            .collect::<HashSet<_>>();
        let bottom_half = pattern
            .iter()
            .filter(|(_, y)| y >= &y_ref && y - y_ref < max_dist)
            .map(|(x, y)| (*x, y_ref - (y - y_ref) - 1))
            .collect::<HashSet<_>>();

        if top_half.symmetric_difference(&bottom_half).count() == differences {
            return y_ref as i32 * 100;
        }
    }

    panic!("No reflection found");
    return 0;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 405);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 400)
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2023_13") {
        RelativePath::new("../../Inputs/2023_13.txt")
    } else {
        RelativePath::new("/Inputs/2023_13.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nNotes summary: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nNotes summary: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
