use itertools::Itertools;
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Intcode {
    mem: HashMap<i64, i64>,
    pc: i64,
}

impl Intcode {
    pub fn new(mem: Vec<i64>) -> Intcode {
        Intcode {
            mem: mem
                .into_iter()
                .enumerate()
                .map(|(i, x)| (i as i64, x))
                .collect(),
            pc: 0,
        }
    }

    pub fn insert(&mut self, k: i64, v: i64) {
        self.mem.insert(k, v);
    }

    pub fn get(&self, k: i64) -> Option<&i64> {
        return self.mem.get(&k);
    }

    pub fn run(&mut self) {
        loop {
            let opcode: i64 = *self.mem.get(&self.pc).unwrap();
            if opcode == 99 {
                break;
            }

            let (reg_a, reg_b, res_reg) = (self.pc + 1..=self.pc + 3)
                .map(|ix| parse_reg(*self.mem.get(&ix).unwrap()))
                .collect_tuple()
                .unwrap();

            let op_a = *self.mem.get(&reg_a).unwrap();
            let op_b = *self.mem.get(&reg_b).unwrap();

            match opcode {
                1 => self.mem.insert(res_reg, op_a + op_b),
                2 => self.mem.insert(res_reg, op_a * op_b),
                _ => panic!("Opcode {} is invalid", opcode),
            };

            self.pc += 4;
        }
    }
}

fn parse_reg(n: i64) -> i64 {
    return n;
}

#[cfg(test)]
mod tests {
    use super::*;
}
