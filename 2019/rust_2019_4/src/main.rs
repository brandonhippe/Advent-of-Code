use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let mut total: i64 = 0;
    let mut i = contents.split("-").nth(0).unwrap().parse::<i64>().unwrap();
    let end = contents.split("-").nth(1).unwrap().parse::<i64>().unwrap();

    while i < end {
        let mut has_double = false;
        let mut no_change = true;
        for ix in 0..5 {
            let a = (i / 10i64.pow(5 - ix)) % 10;
            let b = (i / 10i64.pow(4 - ix)) % 10;
            if a > b {
                i += (a - b) * 10i64.pow(4 - ix);
                has_double = false;
                no_change = false;
                break;
            } else if a == b {
                has_double = true;
            }
        }

        total += has_double as i64;
        i += no_change as i64;
    }

    return total;
}

fn part2(contents: String) -> i64 {
    let mut total: i64 = 0;
    let mut total: i64 = 0;
    let mut i = contents.split("-").nth(0).unwrap().parse::<i64>().unwrap();
    let end = contents.split("-").nth(1).unwrap().parse::<i64>().unwrap();

    while i < end {
        let mut has_double = false;
        let mut no_change = true;
        for ix in 0..5 {
            let a = (i / 10i64.pow(5 - ix)) % 10;
            let b = (i / 10i64.pow(4 - ix)) % 10;
            if a > b {
                i += (a - b) * 10i64.pow(4 - ix);
                has_double = false;
                no_change = false;
                break;
            } else if a == b {
                has_double = has_double
                    || ((ix == 0 || (i / 10i64.pow(6 - ix)) % 10 != a)
                        && (ix == 4 || (i / 10i64.pow(3 - ix)) % 10 != a));
            }
        }

        total += has_double as i64;
        i += no_change as i64;
    }

    return total;
}

fn main() {
    let year = "2019".to_string();
    let day = "4".to_string();

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
        "\nPart 1:\nNumber of valid passwords within range: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nNumber of valid passwords within range: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
