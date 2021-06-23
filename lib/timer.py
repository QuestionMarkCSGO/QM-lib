import asyncio
import time
import inspect
import logging as log

log.basicConfig(level=log.INFO, format='%(levelname)s: %(message)s')

if __name__ == 'lib.timer':
    log.info('timer.py loaded')


class Timer:
    def __init__(self, time, callback=None, end_func=None, name='Timer', first_immediately=False):
        self.time = time
        self.first_immediately = first_immediately
        self.name = name
        if callback:
            self.callback = callback
        else:
            self.callback = self.def_callback
        if end_func:
            self.end_func = end_func
        else:
            self.end_func = self.def_end_func
        self.is_active = True
        self.task = asyncio.ensure_future(self.job())
        log.info('Timer: ' + name + " - init done")


    async def job(self):
        try:
            while self.is_active:
                if self.time <= 0:
                    self.task.cancle()
                    if inspect.iscoroutinefunction(self.end_func):
                        await self.end_func(self)
                    else:
                        self.end_func(self)
                if self.time > 0:
                    await asyncio.sleep(1)
                    await self.callback(self, self.time)
                    self.time -= 1
        except Exception as ex:
            log.warning(ex)

    def resume(self):
        self.is_active = True
        asyncio.ensure_future(self.job())

    def def_end_func(self, timer):
        print(f'{self.name} End')

    async def def_callback(self, timer, time):
        print(f'Default callback: {str(self.time)}')

    def pause(self):
        self.is_active = False
        self.task.cancle()
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

class OldTimer:
    def __init__(self, time, func=None, type='default'):
        print('init Timer()')
        # Types
        # 5D 10h 15m 16s -> default
        # 5 Day(s) 10 Hour(s) 15 Minute(s) 16 Second(s) -> extended
        # 5:10:15:16 -> simple
        self.is_active = False
        self.func = func

        self.time = time.lower()
        if self.time.endswith('s'):
            self.time = int(self.time[:-1])
        elif self.time.endswith('m'):
            self.time = int(self.time[:-1]) * 60
        elif self.time.endswith('h'):
            self.time = int(self.time[:-1]) * 60 * 60
        elif self.time.endswith('d'):
            self.time = int(self.time[:-1]) * 60 * 60 * 24
        else:
            self.time = int(self.time)

        print(f'Timer obj created with time: {self.time}sec, func: {self.func}')

    async def start(self):
        print(f'start Timer Loop! Time: {self.time}sec')
        self.is_active = True
        await self.loop()

    async def loop(self):
        print(f'time: {self.time}sec')
        await asyncio.sleep(1)
        self.time -= 1
        if self.time > 0 and self.is_active:
            await self.loop()

    async def pause(self):
        self.is_active = False

    async def resume(self):
        self.is_active = True
        self.loop()

    async def pause_toggle(self):
        if self.is_active == True:
            self.is_active = False
        if self.is_active == False:
            self.is_active = True
            await self.loop()

    async def add_time(self, sec: int):
        self.time += sec

    async def rem_time(self, sec: int):
        self.time -= sec

    async def set_time(self, sec: int):
        self.time = sec

    async def get_time_string(self):
        ty_res = time.gmtime(self.time)
        str = time.strftime("%HD %Mm %Ss",ty_res)
        print(res)
        return str

    async def on_end():
        if callable(self.func):
            self.func()
