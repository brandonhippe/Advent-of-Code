use relative_path::RelativePath;
use std::env;
use std::fs;
use std::sync::mpsc::channel;
use std::thread::available_parallelism;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let threads = usize::from(available_parallelism().unwrap());
    let (tx, rx) = channel();

    for ix in 0..threads {
        let contents = contents.clone();

        let tx1 = tx.clone();

        std::thread::spawn(move || {
            let mut thread_ix = ix;
            let threads = threads;

            loop {
                let hash = format!("{:x}", md5::compute(format!("{}{}", contents, thread_ix)));
                if hash.starts_with("00000") {
                    let _ = tx1.send((thread_ix, 5));
                    break;
                } else if tx1.send((thread_ix, -1)).is_err() {
                    break;
                }

                thread_ix += threads;
            }
        });
    }

    while let Ok((pos, val)) = rx.recv() {
        if val != -1 {
            return pos as i64;
        }
    }

    return -1;
}

fn part2(contents: String) -> i64 {
    let threads = usize::from(available_parallelism().unwrap());
    let (tx, rx) = channel();

    for ix in 0..threads {
        let contents = contents.clone();

        let tx1 = tx.clone();

        std::thread::spawn(move || {
            let mut thread_ix = ix;
            let threads = threads;

            loop {
                let hash = format!("{:x}", md5::compute(format!("{}{}", contents, thread_ix)));
                if hash.starts_with("000000") {
                    let _ = tx1.send((thread_ix, 6));
                    break;
                }

                thread_ix += threads;
            }
        });
    }

    while let Ok((pos, val)) = rx.recv() {
        if val != -1 {
            return pos as i64;
        }
    }

    return -1;
}

fn main() {
    let year = "2015".to_string();
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
        "\nPart 1:\nFirst number with hash starting with 5 zeros: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\nFirst number with hash starting with 6 zeros: {}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
