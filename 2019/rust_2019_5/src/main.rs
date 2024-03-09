use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;
use intcode_rust::Intcode;

fn part1(contents: String) -> i64 {
    let mut instructions: Intcode = Intcode::new(
        contents
            .split(",")
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>(),
    );

    let mut input_given = false;

    while !instructions.run() {
        if !input_given {
            input_given = true;
            instructions.set_input(1);
            instructions.run();
        } else {
            panic!("Program did not halt");
        }
    }

    return instructions.get_output().pop().unwrap();
}

fn part2(contents: String) -> i64 {
    let mut instructions: Intcode = Intcode::new(
        contents
            .split(",")
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>(),
    );
    
    let mut input_given = false;

    while !instructions.run() {
        if !input_given {
            input_given = true;
            instructions.set_input(5);
            instructions.run();
        } else {
            panic!("Program did not halt");
        }
    }

    return instructions.get_output().pop().unwrap();
}

fn main() {
    let year = "2019".to_string();
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
        "\nPart 1:\nDiagnostic Code: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nDiagnostic Code: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
