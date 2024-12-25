use intcode_rust::Intcode;
use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let mut intcode = Intcode::new(
        contents
            .split(',')
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>(),
    );

    intcode.set_input(1);
    if !intcode.run() {
        panic!("Program did not halt");
    }

    return intcode.get_output()[0];
}

fn part2(contents: String) -> i64 {
    let mut intcode = Intcode::new(
        contents
            .split(',')
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>(),
    );

    intcode.set_input(2);
    if !intcode.run() {
        panic!("Program did not halt");
    }

    return intcode.get_output()[0];
}

fn main() {
    let year = "2019".to_string();
    let day = "9".to_string();

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
        "\nPart 1:\nDiagnostic Code: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nCoordinates: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}