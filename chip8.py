import pygame
from random import randint
import sys

class chip8():
    keyset = {
        pygame.K_1: 1,
        pygame.K_2: 2,
        pygame.K_3: 3,
        pygame.K_4: 12,
        pygame.K_q: 4,
        pygame.K_w: 5,
        pygame.K_e: 6,
        pygame.K_r: 13,
        pygame.K_a: 7,
        pygame.K_s: 8,
        pygame.K_d: 9,
        pygame.K_f: 14,
        pygame.K_z: 10,
        pygame.K_x: 0,
        pygame.K_b: 11,
        pygame.K_v: 15

    }
    fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
             0x20, 0x60, 0x20, 0x20, 0x70,  # 1
             0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
             0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
             0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
             0xF0, 0x80, 0xF0, 0x10, 0xF8,  # 5
             0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
             0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
             0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
             0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
             0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
             0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
             0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
             0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
             0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
             0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
             ]

    def __init__(self):
        pygame.init()
        self.currentop = 0
        self.draw = True
        self.lastop = 0
        self.opcode = 0
        self.white = (255,255,255)
        self.screen = pygame.display.set_mode((64 * 10, 32 * 10))
        self.key_inputs = [0] * 16  # store key input states
        self.display_buffer = [0] * 32 * 64
        self.memory = [0] * 4096  # memory of 4096 bytes
        self.registers = [0] * 16  # registers, 16 0s
        self.sound_timer = 0  # beeping sound is played when the value is nonzero
        self.delay_timer = 0  # used for timings in games
        self.index = 0  # address register
        self.pc = 0  # program counter
        self.stack = [0] * 16
        self.vx = 0
        self.vy = 0
        self.sp = 0

        self.opfunctions = {
            0x0000: self.op_0nnn,
            0x00E0: self.op_00E0,
            0x000E: self.op_00EE,
            0x1000: self.op_1nnn,
            0x2000: self.op_2nnn,
            0x3000: self.op_3xkk,
            0x4000: self.op_4xkk,
            0x5000: self.op_5xy0,
            0x6000: self.op_6xkk,
            0x7000: self.op_7xkk,
            0x8000: self.op_8nnn,
            0x8001: self.op_8xy1,
            0x8002: self.op_8xy2,
            0x8003: self.op_8xy3,
            0x8004: self.op_8xy4,
            0x8005: self.op_8xy5,
            0x8006: self.op_8xy6,
            0x8007: self.op_8xy7,
            0x800E: self.op_8xyE,
            0x9000: self.op_9xy0,
            0xA000: self.op_Annn,
            0xB000: self.op_Bnnn,
            0xC000: self.op_Cxkk,
            0xD000: self.op_Dxyn,
            0xE000: self.op_Ennn,
            0xE00E: self.op_Ex9E,
            0xE001: self.op_ExA1,
            0xF000: self.op_Fnnn,
            0xF007: self.op_Fx07,
            0xF00A: self.op_Fx0A,
            0xF015: self.op_Fx15,
            0xF018: self.op_Fx18,
            0xF01E: self.op_Fx1E,
            0xF029: self.op_Fx29,
            0xF033: self.op_Fx33,
            0xF055: self.op_Fx55,
            0xF065: self.op_Fx65
        }

    def initialize(self):
        self.pc = 512
        for i in range(80):
            self.memory[i] = self.fonts[i]

    def load_rom(self, file_path):
        file = open(file_path, "rb").read()
        for i, val in enumerate(file):
            self.memory[i + 0x200] = val


    def cycle(self):

        self.draw = False

        self.lastop = hex(self.opcode)

        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]  # opcodes are 2 bytes long so this two bytes and combines them
        self.currentop = hex(self.opcode)

        self.vx = (self.opcode & 0x0f00) >> 8  # extract the 2nd nibble and shift by 8 bits
        self.vy = (self.opcode & 0x00f0) >> 4  # extract the 3rd nibble and shift by 4 bits

        '''
            self.vx and self.vy refer to 2nd and 3rd nibble of opcode. Some opcodes use registers
            so the opcodes refer to register locations in the 2nd and 3rd nibbles.
        '''

        hexop = self.opcode & 0xF000
        try:
            self.opfunctions[hexop]()
        except Exception as e:
            print(f"Invalid opcode {hex(hexop)}!")
            print(e.with_traceback())
            self.pc += 2

        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1


    def op_0nnn(self):
        if self.opcode == 0x0:
            pygame.quit()
            sys.exit()
        if self.opcode == 0xe0:
            self.op_00E0()
            return
        extrop = self.opcode & 0xf00f

        try:
            self.opfunctions[extrop]()
        except:
            print(f"invalid opcode, {hex(self.opcode)}")
            self.pc += 2

    def op_00E0(self):
        '''
        Clear display buffer
        :return:
        '''
        self.display_buffer = [0] * 64 * 32
        self.draw = True
        self.pc += 2

    def op_00EE(self):
        '''
        Return from subroutine
        :return:
        '''
        self.pc = self.stack[self.sp] + 2
        self.sp -= 1


    def op_1nnn(self):
        '''
        Jump to NNN
        :return:
        '''
        self.pc = self.opcode & 0x0FFF


    def op_2nnn(self):
        '''
        Jump to subroutine at NNN
        :return:
        '''
        nnn = self.opcode & 0xfff
        self.sp += 1
        self.stack[self.sp] = self.pc  # store pc before jump at top of the stack
        self.pc = nnn

    def op_3xkk(self):
        '''
        Skip next instruction if VX == KK
        :return:
        '''
        kk = self.opcode & 0x00FF
        if self.registers[self.vx] == kk:
            self.pc += 4
        else:
            self.pc += 2

    def op_4xkk(self):
        '''
        Skip next instruction if VX != KK
        :return:
        '''
        kk = self.opcode & 0x00FF
        if self.registers[self.vx] != kk:
            self.pc += 4
        else:
            self.pc += 2

    def op_5xy0(self):
        '''
        Skip next instruction if VX == VY
        :return:
        '''
        if self.registers[self.vx] == self.registers[self.vy]:
            self.pc += 4
        else:
            self.pc += 2

    def op_6xkk(self):
        '''
        Assigns KK to VX
        :return:
        '''
        kk = self.opcode & 0x00FF
        self.registers[self.vx] = kk
        self.pc += 2

    def op_7xkk(self):
        '''
        Sets VX to VX + KK
        :return:
        '''
        kk = self.opcode & 0x00FF
        self.registers[self.vx] += kk
        self.registers[self.vx] &= 0xff
        self.pc += 2

    def op_8nnn(self):
        if self.opcode & 0x000F == 0:
            self.op_8xy0()
            return

        try:
            self.opfunctions[self.opcode & 0xf00f]()
        except:
            print("Unknown instruction")
            self.pc += 2

    def op_8xy0(self):
        '''
        SETS VX to VY
        :return:
        '''
        self.registers[self.vx] = self.registers[self.vy]
        self.registers[self.vx] &= 0xFF
        self.pc += 2

    def op_8xy1(self):
        '''
        Performs bitwise OR operation on Vx and Vy, then stores the result
        in Vx.
        :return:
        '''
        val = self.registers[self.vx] | self.registers[self.vy]
        self.registers[self.vx] = val
        self.registers[self.vx] &= 0xFF
        self.pc += 2

    def op_8xy2(self):
        '''
        Performs bitwise AND operation on Vx and Vy, then stores the result
        in Vx.
        :return:
        '''
        val = self.registers[self.vx] & self.registers[self.vy]
        self.registers[self.vx] = val
        self.registers[self.vx] &= 0xFF
        self.pc += 2

    def op_8xy3(self):
        '''
        Performs bitwise XOR operation on Vx and Vy, then stores the result
        in Vx.
        :return:
        '''
        val = self.registers[self.vx] ^ self.registers[self.vy]
        self.registers[self.vx] = val
        self.registers[self.vx] &= 0xFF
        self.pc += 2

    def op_8xy4(self):
        '''
        Adds values of Vx and Vy, if the result is > 255(8 bits), set carry flag to 1, else set it to 0.
        Stores the lowest 8 bits of the result in Vx.
        :return:
        '''
        val = self.registers[self.vx] + self.registers[self.vy]
        if val > 0x00FF:
            self.registers[0xF] = 1
        else:
            self.registers[0xF] = 0

        self.registers[self.vx] = val
        self.registers[self.vx] &= 0xFF
        self.pc += 2

    def op_8xy5(self):
        '''
        Sets VX = VX - VY
        If there is not a borrow, set VF to 1, else to 0
        :return:
        '''
        if self.registers[self.vx] < self.registers[self.vy]:
            self.registers[15] = 0
        else:
            self.registers[15] = 1

        self.registers[self.vx] -= self.registers[self.vy]
        self.registers[self.vx] &= 0xFF
        self.pc += 2

    def op_8xy6(self):
        '''
        Sets VF to least significant bit of VX
        Set VX to VX shifted right by 1
        :return:
        '''
        self.registers[0xF] = self.registers[self.vx] & 0x0001
        self.registers[self.vx] = self.registers[self.vx] >> 1
        self.registers[self.vx] &= 0xFF
        self.pc += 2

    def op_8xy7(self):
        '''
        Sets VX = VY - VX
        If there is not a borrow, set VF to 1, else to 0
        :return:
        '''
        if self.registers[self.vy] < self.registers[self.vx]:
            self.registers[15] = 0
        else:
            self.registers[15] = 1

        self.registers[self.vx] = self.registers[self.vy] - self.registers[self.vx]
        self.registers[self.vx] &= 0xff
        self.pc += 2

    def op_8xyE(self):
        '''
        Set VF to most significant bit of VX
        Set VX to VY shifted left by one
        :return:
        '''
        self.registers[0xF] = self.registers[self.vx] >> 7
        self.registers[self.vx] = self.registers[self.vx] << 1
        self.pc += 2

    def op_9xy0(self):
        '''
        Skips next instruction if VX != VY
        :return:
        '''
        if self.registers[self.vx] != self.registers[self.vy]:
            self.pc += 4
        else:
            self.pc += 2

    def op_Annn(self):
        '''
        Sets I to NNN
        :return:
        '''
        self.index = self.opcode & 0x0FFF
        self.pc += 2

    def op_Bnnn(self):
        '''
        Jump to address NNNN + V0
        :return:
        '''
        self.pc = (self.opcode & 0x0FFF) + self.registers[0]

    def op_Cxkk(self):
        '''
        Sets VX to random number between 0x0 and 0xFF  and masks it with NN
        :return:
        '''
        rnum = randint(0, 255)
        self.registers[self.vx] = rnum & (self.opcode & 0x00FF)
        self.pc += 2

    def op_Dxyn(self):
        '''
        Draws 8xN
        :return:
        '''
        x = self.registers[self.vx]
        y = self.registers[self.vy]
        self.registers[0xF] = 0
        height = self.opcode & 0x000F

        for h in range(height):
            pixel = self.memory[self.index + h]
            for w in range(8):
                if (pixel & (0x80 >> w)) != 0:

                    loc = (x + w + (h + y) * 64) % 2048

                    if self.display_buffer[loc] == 1:
                        self.registers[0xf] = 1
                    self.display_buffer[loc] ^= 1

        self.draw = True
        self.pc += 2

    def op_Ennn(self):
        '''
        Decode Ennn-opcodes
        :return:
        '''
        try:
            self.opfunctions[self.opcode & 0xf00f]()
        except Exception as e:
            print(e.with_traceback())
            print(f"invalid opcode {hex(self.opcode)}")

    def op_Ex9E(self):
        '''
        Skip next instruction if key stored in Vx is pressed
        :return:
        '''
        if self.key_inputs[self.registers[self.vx] & 0xf] != 0:
            self.pc += 4
        else:
            self.pc += 2

    def op_ExA1(self):
        '''
        Skip next instruction if key stored in Vx is not pressed
        :return:
        '''
        if self.key_inputs[self.registers[self.vx] & 0xf] == 0:
            self.pc += 4
        else:
            self.pc += 2

    def op_Fnnn(self):
        '''
        Decode Fnnn-opcodes
        :return:
        '''
        try:
            self.opfunctions[self.opcode & 0xf0ff]()
        except Exception as e:
            print(" Opcode was not valid why?")
            print(e.with_traceback())

    def op_Fx07(self):
        '''
        Store delay timer in register VX
        :return:
        '''
        self.registers[self.vx] = self.delay_timer
        self.pc += 2

    def op_Fx0A(self):
        '''
        Wait for a keypress
        :return:
        '''
        while (True):
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key in self.keyset.keys():
                    self.key_inputs[self.keyset[event.key]] = 1
                    break
        self.pc += 2

    def op_Fx15(self):
        '''
        Store register VX in delay timer
        :return:
        '''
        self.delay_timer = self.registers[self.vx]
        self.pc += 2

    def op_Fx18(self):
        '''
        Store register VX in sound timer
        :return:
        '''
        self.sound_timer = self.registers[self.vx]
        self.pc += 2

    def op_Fx1E(self):
        '''
        Add register VX to register I
        :return:
        '''
        self.index += self.registers[self.vx]
        self.pc += 2

    def op_Fx29(self):
        '''
        Store sprite location in register I
        :return:
        '''
        self.index = (5 * (self.registers[self.vx])) & 0x0FFF
        self.pc += 2

    def op_Fx33(self):

        '''
        Store BCD of register VX in I..I+2
        :return:
        '''
        self.memory[self.index] = self.registers[self.vx] // 100
        self.memory[self.index + 1] = (self.registers[self.vx] % 100) // 10
        self.memory[self.index + 2] = self.registers[self.vx] % 10
        self.pc += 2

    def op_Fx55(self):
        '''
        Store registers V0 to VX in memory starting at location I
        :return:
        '''
        i = 0
        while i <= self.vx:
            self.memory[self.index + i] = self.registers[i]
            i += 1

        self.pc += 2

    def op_Fx65(self):
        '''
        Store memory values starting at location I in registers V0 to VX
        :return:
        '''
        i = 0
        while i <= self.vx:
            self.registers[i] = self.memory[self.index + i]
            i += 1
        self.pc += 2


    def drawScreen(self):
        '''
        Draw the sprites on the window using PYGAME
        :return:
        '''
        black = (0, 0, 0)
        white = (255, 255, 255)
        self.screen.fill(black)
        for i in range(len(self.display_buffer)):
                if self.display_buffer[i] == 1:
                    pygame.draw.rect(self.screen, white, ((i % 64) * 10, (i / 64) * 10, 10,10))
                else:
                    pygame.draw.rect(self.screen, black, ((i % 64) * 10, (i / 64) * 10, 10,10))

        pygame.display.update()


    def main(self):
        rompath = sys.argv[1]
        self.initialize()
        self.load_rom(rompath)
        timer = pygame.time.Clock()
        time = 0
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keyset.keys():
                        self.key_inputs[self.keyset[event.key]] = 1

                if event.type == pygame.KEYUP:
                    if event.key in self.keyset.keys():
                        self.key_inputs[self.keyset[event.key]] = 0

            self.cycle()
            if self.draw:
                self.drawScreen()





def main():
    cpu = chip8()
    chip8.main(cpu)


if __name__ == '__main__':
    main()
