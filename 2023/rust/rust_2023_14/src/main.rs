use relative_path::RelativePath;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let mut stationary: HashSet<(i32, i32)> = HashSet::new();
    let mut rocks: HashSet<(i32, i32)> = HashSet::new();

    for (y, line) in contents.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            match c {
                '#' => stationary.insert((x as i32, y as i32)),
                'O' => rocks.insert((x as i32, y as i32)),
                _ => true,
            };
        }
    }

    let max_ix = contents.lines().count() as i32;
    rocks = roll(&stationary, &rocks, [0, -1], max_ix - 1);

    return rocks.iter().map(|(_, y)| max_ix - y).sum();
}

fn part2(contents: String) -> i32 {
    let mut stationary: HashSet<(i32, i32)> = HashSet::new();
    let mut rocks: HashSet<(i32, i32)> = HashSet::new();
    let dir_arr = [[0, -1], [-1, 0], [0, 1], [1, 0]];

    for (y, line) in contents.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            match c {
                '#' => stationary.insert((x as i32, y as i32)),
                'O' => rocks.insert((x as i32, y as i32)),
                _ => true,
            };
        }
    }

    let max_ix = contents.lines().count() as i32;
    let mut seen: HashMap<Vec<(i32, i32)>, i32> = HashMap::new();
    let goal_iterations = 1_000_000_000;

    for cycle in 1..=goal_iterations {
        for dir in dir_arr.iter() {
            rocks = roll(&stationary, &rocks, *dir, max_ix - 1);
        }

        let hash_rocks: Vec<(i32, i32)> = convert_to_hashable(&rocks);

        if seen.contains_key(&hash_rocks) {
            let cycle_len = cycle - seen.get(&hash_rocks).unwrap();
            let remaining = (goal_iterations - cycle) % cycle_len;

            for _ in 0..remaining {
                for dir in dir_arr.iter() {
                    rocks = roll(&stationary, &rocks, *dir, max_ix - 1);
                }
            }

            break;
        } else {
            seen.insert(hash_rocks.clone(), cycle);
        }
    }

    return rocks.iter().map(|(_, y)| max_ix - y).sum();
}

fn convert_to_hashable(rocks: &HashSet<(i32, i32)>) -> Vec<(i32, i32)> {
    let mut new_rocks: Vec<(i32, i32)> = Vec::new();

    for (x, y) in rocks {
        new_rocks.push((*x, *y));
    }

    new_rocks.sort();
    return new_rocks;
}

fn roll(
    stationary: &HashSet<(i32, i32)>,
    rocks: &HashSet<(i32, i32)>,
    direction: [i32; 2],
    max_ix: i32,
) -> HashSet<(i32, i32)> {
    let mut new_rocks: HashSet<(i32, i32)> = HashSet::new();

    for i in 0..=max_ix {
        let direction_sum = direction.iter().sum::<i32>();
        let mut next_pos = if direction_sum > 0 { max_ix } else { 0 };

        for j in 0..=max_ix {
            let ix = if direction_sum > 0 { max_ix - j } else { j };
            let pos: (i32, i32) = if direction[0] == 0 { (i, ix) } else { (ix, i) };

            if stationary.contains(&pos) {
                next_pos = ix - direction_sum;
            } else if rocks.contains(&pos) {
                if direction[0] == 0 {
                    new_rocks.insert((pos.0, next_pos));
                } else {
                    new_rocks.insert((next_pos, pos.1));
                }

                next_pos -= direction_sum;
            }
        }
    }

    return new_rocks;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 136);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 64)
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2023_14") {
        RelativePath::new("../../Inputs/2023_14.txt")
    } else {
        RelativePath::new("/Inputs/2023_14.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nLoad after shifting north: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nLoad after 1,000,000,000 cycles: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
