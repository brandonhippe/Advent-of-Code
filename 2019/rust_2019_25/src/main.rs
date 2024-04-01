use relative_path::RelativePath;
use std::env;
use std::fs;
use std::time::Instant;
use intcode_rust::Intcode;

fn part1(contents: String) -> i64 {
    let mut program = Intcode::new(contents.split(",").map(|x| x.parse().unwrap()).collect());

    while !program.run() {
        let output = program.get_output();
        print!("{}", output.iter().map(|x| *x as u8 as char).collect::<String>());
        program.clear_output();

        let mut input = String::new();
        std::io::stdin().read_line(&mut input).unwrap();
        input = input.trim().to_string();

        for c in input.chars() {
            program.set_input(c as i64);
            program.run();
        }

        program.set_input(10);
    }

    let output = program.get_output();
    print!("{}", output.iter().map(|x| *x as u8 as char).collect::<String>());

    return 0;
}

fn part2(_contents: String) -> String {
    return "Christmas has been saved!".to_string();
}

fn main() {
    let year = "2019".to_string();
    let day = "25".to_string();

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
