use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Intcode {
    mem: HashMap<i64, i64>,
    pc: i64,
    input: i64,
    outputs: Vec<i64>,
    handler: fn(&mut Intcode) -> (),
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
            input: 0,
            outputs: Vec::new(),
            handler: default_handler,
        }
    }

    pub fn set_handler(&mut self, handler: fn(&mut Intcode) -> ()){
        self.handler = handler;
    }

    pub fn insert(&mut self, k: i64, v: i64) {
        self.mem.insert(k, v);
    }

    pub fn set_input(&mut self, input: i64) {
        self.input = input;
    }

    pub fn get_output(&self) -> Vec<i64> {
        return self.outputs.clone();
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

            let (res_reg, op_a, op_b) = self.parse_op(opcode);

            match opcode % 100 {
                1 => {
                    // ADD
                    self.mem.insert(res_reg, op_a.unwrap() + op_b.unwrap());
                    self.pc += 4;
                },
                2 => {
                    // MULT
                    self.mem.insert(res_reg, op_a.unwrap() * op_b.unwrap());
                    self.pc += 4;
                },
                3 => {
                    // INPUT
                    (self.handler)(self);
                    self.mem.insert(res_reg, self.input);
                    self.pc += 2;
                },
                4 => {
                    // OUTPUT
                    self.outputs.push(self.mem.get(&res_reg).unwrap().clone());
                    self.pc += 2;
                },
                5 => {
                    // JMP IF TRUE
                    self.pc = if op_a.unwrap() != 0 { op_b.unwrap() } else { self.pc + 3 };
                },
                6 => {
                    // JMP IF FALSE
                    self.pc = if op_a.unwrap() == 0 { op_b.unwrap() } else { self.pc + 3 };
                },
                7 => {
                    // LESS THAN
                    self.mem.insert(res_reg, if op_a.unwrap() < op_b.unwrap() { 1 } else { 0 });
                    self.pc += 4;
                },
                8 => {
                    // EQUALS
                    self.mem.insert(res_reg, if op_a.unwrap() == op_b.unwrap() { 1 } else { 0 });
                    self.pc += 4;
                },
                _ => panic!("Opcode {} is invalid", opcode),
            };
        }
    }

    fn parse_op(&self, opcode: i64) -> (i64, Option<i64>, Option<i64>) {
        let op1 = *self.mem.get(&(self.pc + 1)).unwrap();
        let op2 = *self.mem.get(&(self.pc + 2)).unwrap();
        let op3 = *self.mem.get(&(self.pc + 3)).unwrap();

        let mode_1 = (opcode / 100) % 10;
        let mode_2 = (opcode / 1000) % 10;
        let _mode_3 = (opcode / 10000) % 10;

        match opcode % 100 {
            3 | 4 => {
                return (op1, None, None);
            },
            _ => {
                return (
                    op3,
                    match mode_1 {
                        0 => self.mem.get(&op1).cloned(),
                        1 => Some(op1),
                        _ => panic!("Invalid mode {}", mode_1),
                    },
                    match mode_2 {
                        0 => self.mem.get(&op2).cloned(),
                        1 => Some(op2),
                        _ => panic!("Invalid mode {}", mode_2),
                    },
                );
            },
        }
    }
}

fn default_handler(ic: &mut Intcode) {
    ic.run();
}


#[cfg(test)]
mod tests {
    use super::*;
}
