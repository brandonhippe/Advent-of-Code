use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;
use intcode_rust::Intcode;

fn part1(contents: String) -> i64 {
    let mut program = Intcode::new(contents.split(",").map(|x| x.parse().unwrap()).collect());
    let input_string = "NOT B J\nNOT C T\nOR T J\nAND D J\nNOT A T\nOR T J\nWALK\n".to_string();

    for c in input_string.chars() {
        program.run();
        program.set_input(c as i64);
    }

    if program.run() {
        let output = program.get_output();
        if output.last().unwrap() > &127 {
            return *output.last().unwrap();
        }
        
        for c in output {
            print!("{}", c as u8 as char);
        }
    } else {
        panic!("Program did not finish");
    }

    return -1;
}

fn part2(contents: String) -> i64 {
    let mut program = Intcode::new(contents.split(",").map(|x| x.parse().unwrap()).collect());
    let input_string = "NOT B J\nNOT C T\nOR T J\nAND D J\nAND H J\nNOT A T\nOR T J\nRUN\n".to_string();

    for c in input_string.chars() {
        program.run();
        program.set_input(c as i64);
    }

    if program.run() {
        let output = program.get_output();
        if output.last().unwrap() > &127 {
            return *output.last().unwrap();
        }
        
        for c in output {
            print!("{}", c as u8 as char);
        }
    } else {
        panic!("Program did not finish");
    }

    return -1;
}

fn main() {
    let year = "2019".to_string();
    let day = "21".to_string();

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
        "\nPart 1:\nHull Damage: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nHull Damage: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
