use nalgebra::DMatrix;
use relative_path::RelativePath;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::time::Instant;

fn part1(contents: String) -> i64 {
    let mut connections: HashMap<String, HashSet<String>> = HashMap::new();
    for line in contents.lines() {
        let s1: String = line.split(":").nth(0).unwrap().to_string();
        let others: Vec<String> = line
            .split(": ")
            .nth(1)
            .unwrap()
            .split(" ")
            .map(|s| s.to_string())
            .collect();

        for other in others {
            connections
                .entry(s1.clone())
                .or_insert(HashSet::new())
                .insert(other.clone());
            connections
                .entry(other.clone())
                .or_insert(HashSet::new())
                .insert(s1.clone());
        }
    }

    let mapping: Vec<String> = connections.keys().map(|s| s.to_string()).collect();
    let arr_dim = connections.len();
    let mut degree: DMatrix<f64> = DMatrix::from_element(arr_dim, arr_dim, 0.0);
    let mut adj: DMatrix<f64> = DMatrix::from_element(arr_dim, arr_dim, 0.0);

    for (i, k) in mapping.iter().enumerate() {
        degree[(i, i)] = connections.get(k).unwrap().len() as f64;

        for n in connections.get(k).unwrap() {
            let j = mapping.iter().position(|x| x == n).unwrap();
            adj[(j, i)] = 1.0;
        }
    }

    let laplacian = degree - adj;
    let eigen_decomp = laplacian.symmetric_eigen();
    let eigenvalues = eigen_decomp.eigenvalues;
    let eigenvectors = eigen_decomp.eigenvectors;

    let mut min_ix = 0;
    let mut min_2_ix = 0;

    for ix in 0..eigenvalues.len() {
        if eigenvalues[ix] < eigenvalues[min_ix] {
            min_2_ix = min_ix;
            min_ix = ix;
        } else if eigenvalues[ix] < eigenvalues[min_2_ix] {
            min_2_ix = ix;
        }
    }

    let fiedler_vector = eigenvectors.column(min_2_ix);
    let g_size = fiedler_vector.iter().filter(|x| x > &&0.0).count() as i64;

    return g_size * (arr_dim as i64 - g_size);
}

fn part2(_contents: String) -> String {
    return "Christmas has been saved!".to_string();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_test() {
        let contents =
            fs::read_to_string("example.txt").expect("Should have been able to read the file");

        assert_eq!(part1(contents), 54);
    }
}

fn main() {
    let root = env::current_dir().unwrap();
    let relative_path = if root.ends_with("rust_2023_25") {
        RelativePath::new("../../Inputs/2023_25.txt")
    } else {
        RelativePath::new("/Inputs/2023_25.txt")
    };

    let contents = fs::read_to_string(relative_path.to_path(&root))
        .expect("Should have been able to read the file");

    let part1_timer = Instant::now();
    println!(
        "\nPart 1:\nProduct of group sizes: {}\nRan in {:.5?}",
        part1(contents.clone()),
        part1_timer.elapsed()
    );

    let part2_timer = Instant::now();
    println!(
        "\nPart 2:\n{}\nRan in {:.5?}",
        part2(contents.clone()),
        part2_timer.elapsed()
    );
}
