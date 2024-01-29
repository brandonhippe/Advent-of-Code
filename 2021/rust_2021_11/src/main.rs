use relative_path::RelativePath;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i32 {
    let mut octopi: HashMap<(i32, i32), i32> = HashMap::new();

    for (y, line) in contents.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            octopi.insert((x as i32, y as i32), c.to_digit(10).unwrap() as i32);
        }
    }

    let mut flashes: i32 = 0;
    for _ in 0..100 {
        let mut flashing: VecDeque<(i32, i32)> = VecDeque::new();

        for (pos, num) in octopi.clone().iter() {
            let new_num = *num + 1;
            octopi.insert(*pos, new_num);

            if new_num == 10 {
                flashing.push_front(*pos);
            }
        }

        let mut flashed: HashSet<(i32, i32)> = HashSet::new();
        while let Some(p) = flashing.pop_back() {
            if flashed.contains(&p) {
                continue;
            }

            flashed.insert(p);

            for i in -1..=1 {
                for j in -1..=1 {
                    if i == 0 && j == 0 {
                        continue;
                    }

                    let n = (p.0 + i, p.1 + j);
                    if octopi.contains_key(&n) {
                        let num = octopi.get(&n).unwrap() + 1;
                        octopi.insert(n, num);

                        if num >= 10 {
                            flashing.push_front(n);
                        }
                    }
                }
            }
        }

        flashes += flashed.len() as i32;

        for pos in flashed.iter() {
            octopi.insert(*pos, 0);
        }
    }

    return flashes;
}

fn part2(contents: String) -> i32 {
    let mut octopi: HashMap<(i32, i32), i32> = HashMap::new();

    for (y, line) in contents.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            octopi.insert((x as i32, y as i32), c.to_digit(10).unwrap() as i32);
        }
    }

    let mut step: i32 = 0;
    loop {
        let mut flashing: VecDeque<(i32, i32)> = VecDeque::new();

        for (pos, num) in octopi.clone().iter() {
            let new_num = *num + 1;
            octopi.insert(*pos, new_num);

            if new_num == 10 {
                flashing.push_front(*pos);
            }
        }

        let mut flashed: HashSet<(i32, i32)> = HashSet::new();
        while let Some(p) = flashing.pop_back() {
            if flashed.contains(&p) {
                continue;
            }

            flashed.insert(p);

            for i in -1..=1 {
                for j in -1..=1 {
                    if i == 0 && j == 0 {
                        continue;
                    }

                    let n = (p.0 + i, p.1 + j);
                    if octopi.contains_key(&n) {
                        let num = octopi.get(&n).unwrap() + 1;
                        octopi.insert(n, num);

                        if num >= 10 {
                            flashing.push_front(n);
                        }
                    }
                }
            }
        }

        step += 1;

        if flashed.len() == octopi.len() {
            return step;
        }

        for pos in flashed.iter() {
            octopi.insert(*pos, 0);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 1656);
    }

    #[test]
    fn p2_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part2(contents), 195);
    }
}

fn main() {
    // main_repeat();
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2021_11") {
        RelativePath::new("../../Inputs/2021_11.txt")
    } else {
        RelativePath::new("/Inputs/2021_11.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\n {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\n {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
