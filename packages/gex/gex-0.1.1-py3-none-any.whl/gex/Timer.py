"""Short module for time measurements."""

import time
from typing import NamedTuple, List
from typing_extensions import Self
from dataclasses import dataclass, field



@dataclass
class TimeStamp:
    """Struct with time and msg."""

    t: float
    msg: str = "Tick"


@dataclass
class Timer:
    """Calling TICKs and stroring values."""
    process_name: str = "DEF TIMER"
    t_chain: List[TimeStamp] = field(default_factory=list)
    t0: int | None = None

    def print(self, msg: str, *args):
        print(f">T>>{self.process_name}:: "+msg,*args)

    def reset(self, start_msg: str = "Start"):
        self.t_chain = []
        self.tick(start_msg)
        
    def log(self, msg: str): self.tick(msg, verbose = False)
    def tick(self, msg: str = "tick", verbose: bool = True):
        if self.t0 is None: self.t0 = time.perf_counter()
        new_stamp = TimeStamp(time.perf_counter()-self.t0, msg)

        if verbose:
            if len(self.t_chain) > 0:
                self.print(f" .. --> {msg}\
                    \n dt= { new_stamp.t - self.t_chain[-1].t :.3f} [s]\
                    \n x-1= {self.t_chain[-1].msg}"
                )
            else:
                self.print(f"Timer:{self.process_name}: {msg}")
        self.t_chain += [new_stamp]

    def track(self, block_name) -> Self:
        self.process_name = block_name
        return self

    def __enter__(self):
        self.tick("START : "+ self.process_name)
    def __exit__(self,*args):
        self.tick(f"END : {self.process_name}")

    def show(self):
        print("\n>T>> TICK LIST")
        for tick in self.t_chain:
            print(tick)

if __name__=='__main__':
    timer = Timer("FOO")

    timer.tick("message 1")

    with timer.track("process 1"):
        timer.tick("message 2")
    
    with timer.track("process 2"):
        print("in process 2")

    timer.tick("program end")

    timer.show()